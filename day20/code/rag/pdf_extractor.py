import os
import uuid

import pymupdf as fitz
import pdfplumber
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

import config
import descriptions


def _table_to_markdown(table_rows):
    rows = [[cell if cell is not None else "" for cell in row] for row in table_rows]
    header, *body = rows
    lines = ["| " + " | ".join(header) + " |", "| " + " | ".join(["---"] * len(header)) + " |"]
    for row in body:
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def extract_text_chunks(pdf_path, filename):
    loader = PyMuPDFLoader(pdf_path)
    pages = loader.load()  # one LangChain Document per page

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
    )

    chunks = []
    for page in pages:
        page_number = page.metadata.get("page", 0) + 1  # loader pages are 0-indexed
        for chunk_text in splitter.split_text(page.page_content):
            if not chunk_text.strip():
                continue
            chunks.append(
                Document(
                    page_content=chunk_text,
                    metadata={
                        "source": filename,
                        "page": page_number,
                        "content_type": "text",
                        "doc_id": str(uuid.uuid4()),
                    },
                )
            )
    return chunks


def extract_table_chunks(pdf_path, filename):
    """Use pdfplumber to find tables on every page and turn each one into a
    Document whose text is a markdown version of the table."""
    chunks = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            for table in page.extract_tables():
                if not table or len(table) < 2 or len(table[0]) < 2:
                    continue  # need at least a header row + one data row, and 2+ columns

                # pdfplumber sometimes mistakes a plain text box or a line of
                # graphics for a table. Skip anything that's mostly empty -
                # a real table has a decent amount of text in its cells.
                cell_text = "".join(cell.strip() for row in table for cell in row if cell)
                if len(cell_text) < 20:
                    continue

                markdown_table = _table_to_markdown(table)

                description = None
                if config.GENERATE_DESCRIPTIONS:
                    description = descriptions.describe_table(markdown_table)

                content = f"Table found on page {page_number} of {filename}."
                if description:
                    content += f" {description}"
                content += f"\n\n{markdown_table}"

                metadata = {
                    "source": filename,
                    "page": page_number,
                    "content_type": "table",
                    "doc_id": str(uuid.uuid4()),
                    # Kept separately (raw, no description prefix) so the UI
                    # can render just the table under the AI description,
                    # without repeating the description text twice.
                    "table_markdown": markdown_table,
                }
                if description:
                    metadata["description"] = description

                chunks.append(Document(page_content=content, metadata=metadata))
    return chunks


def extract_image_chunks(pdf_path, filename):
    """Use PyMuPDF to pull embedded images out of the PDF. Small decorative
    icons are skipped (see MIN_IMAGE_WIDTH/HEIGHT in config.py) so we only
    keep real figures/photos/diagrams. Each kept image is saved as a .png
    file. If enabled, a local vision model describes what the image
    actually shows (see descriptions.py); that description - plus the
    surrounding page text as extra context - becomes the chunk's
    searchable text."""
    chunks = []
    stem = os.path.splitext(filename)[0]
    output_dir = os.path.join(config.IMAGES_FOLDER, stem)
    os.makedirs(output_dir, exist_ok=True)

    pdf_doc = fitz.open(pdf_path)
    try:
        for page_index in range(len(pdf_doc)):
            page = pdf_doc[page_index]
            page_number = page_index + 1
            page_text = page.get_text().strip().replace("\n", " ")

            for image_index, image_info in enumerate(page.get_images(full=True), start=1):
                xref = image_info[0]
                pixmap = fitz.Pixmap(pdf_doc, xref)

                if pixmap.width < config.MIN_IMAGE_WIDTH or pixmap.height < config.MIN_IMAGE_HEIGHT:
                    continue  # too small to be a meaningful figure

                # PNG only supports grayscale or RGB. PDFs can embed images
                # in other color spaces (CMYK, Indexed, Separation/spot
                # colors, ...), so convert anything that isn't already
                # plain gray or RGB before saving.
                colorspace_name = pixmap.colorspace.name if pixmap.colorspace else None
                if colorspace_name not in ("DeviceGray", "DeviceRGB"):
                    pixmap = fitz.Pixmap(fitz.csRGB, pixmap)

                image_filename = f"page{page_number}_img{image_index}.png"
                image_path = os.path.join(output_dir, image_filename)
                pixmap.save(image_path)

                description = None
                if config.GENERATE_DESCRIPTIONS:
                    description = descriptions.describe_image(image_path)

                caption = f"Image found on page {page_number} of {filename}."
                if description:
                    caption += f" {description}"
                caption += f" Nearby text on that page: {page_text[:300]}"

                metadata = {
                    "source": filename,
                    "page": page_number,
                    "content_type": "image",
                    "image_path": image_path,
                    "doc_id": str(uuid.uuid4()),
                }
                if description:
                    metadata["description"] = description

                chunks.append(Document(page_content=caption, metadata=metadata))
    finally:
        pdf_doc.close()
    return chunks


def extract_all_chunks(pdf_path):
    """Run all three extractors on one PDF and return a single combined list
    of Documents, ready to be embedded and stored in Chroma."""
    filename = os.path.basename(pdf_path)
    return (
        extract_text_chunks(pdf_path, filename)
        + extract_table_chunks(pdf_path, filename)
        + extract_image_chunks(pdf_path, filename)
    )
