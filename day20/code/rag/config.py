import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_FOLDER = os.path.join(BASE_DIR, "files")
IMAGES_FOLDER = os.path.join(BASE_DIR, "extracted_images")
CHROMA_FOLDER = os.path.join(BASE_DIR, "chroma_db")
COLLECTION_NAME = "pdf_knowledge_base"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150
MIN_IMAGE_WIDTH = 150
MIN_IMAGE_HEIGHT = 150
TOP_K_RESULTS = 5
LLM_MODEL = "qwen2.5:7b"
VISION_MODEL = "moondream"
GENERATE_DESCRIPTIONS = True
