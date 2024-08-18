from pathlib import Path
from llama_index.readers.file import PyMuPDFReader

def load_documents(file_path: str):
    loader = PyMuPDFReader()
    documents = loader.load(file_path=file_path)
    return documents
