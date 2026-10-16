import os

import config
import knowledge_base


def main():
    vectorstore = knowledge_base.get_vectorstore()
    already_ingested = set(knowledge_base.list_documents(vectorstore))

    pdf_files = [f for f in os.listdir(config.PDF_FOLDER) if f.lower().endswith(".pdf")]
    print(f"Found {len(pdf_files)} PDF file(s) in '{config.PDF_FOLDER}/'.")

    for filename in sorted(pdf_files):
        if filename in already_ingested:
            print(f"  - {filename}: already in the knowledge base, skipping.")
            continue

        pdf_path = os.path.join(config.PDF_FOLDER, filename)
        print(f"  - {filename}: ingesting...")
        num_chunks = knowledge_base.add_document(vectorstore, pdf_path)
        print(f"    added {num_chunks} chunks.")

    print("Done. Run `streamlit run app.py` to try the demo.")


if __name__ == "__main__":
    main()
