from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import CHUNK_OVERLAP_SIZE, CHUNK_SIZE
from langchain_core.documents import Document

import pymupdf as fitz
import os
import uuid

import logging
logger = logging.getLogger(__name__)

def extract_text_info(file_path: str):
    # create the loader
    loader = PyMuPDFLoader(file_path)

    # load the contents from all the pages
    pages = loader.load()

    # create the splitter
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP_SIZE
    )

    # create the chunks collection
    chunks = []

    # extract the contents page by page
    for page in pages:
        # get the page number
        page_number = page.metadata.get("page", 0) + 1

        # get the contents
        for text_content in splitter.split_text(page.page_content):

            # create a chunk document from the text content
            chunks.append(
                Document(
                    page_content=text_content,
                    metadata= {
                        "source": str(file_path),
                        "page_number": page_number,
                        "content_type": "text",
                        "doc_id": str(uuid.uuid4()),
                    }
                )
            )

    return chunks

def extract_images_from_pdf_file(file_path: str):
    # create chunks 
    chunks = []

    # load the pdf file
    pdf_doc = fitz.open(file_path)

    logger.info("extracting images")

    # read the contents page by page
    for page_index in range(len(pdf_doc)):

        # get the page at page_index
        page = pdf_doc[page_index]
        
        # get the page_number
        page_number = page_index + 1

        # get the page text
        page_text = page.get_text().strip().replace("\n", " ")

        # get the images
        for image_index, image_info in enumerate(page.get_images(full=True), start=1):
            # get the pixmap from the document for the image
            pixmap = fitz.Pixmap(pdf_doc, image_info[0])

            # get the color space
            colorspace_name = pixmap.colorspace.name if pixmap.colorspace else None
            if colorspace_name not in ("DeviceGray", "DeviceRGB"):
                pixmap = fitz.Pixmap(fitz.csRGB, pixmap)

            caption = f" Nearby text on that page: {page_text[:300]}"

            image_filename = f"page{page_number}_img{image_index}.png"
            image_path = os.path.join("images", image_filename)
            pixmap.save(image_path)

            # create the metadata
            metadata = {
                "source": str(file_path),
                "page": page_number,
                "content_type": "image",
                "image_path": str(image_path),
                "doc_id": str(uuid.uuid4()),
            }

            # append the image to the chunk
            chunks.append(Document(page_content=caption, metadata=metadata))

    return chunks

def extract_all_chunks_from_pdf_file(file_path: str):
    # read the contents of the file
    # extract the images from the file
    # create the chunks of textual contents
    return extract_text_info(file_path) + extract_images_from_pdf_file(file_path)
