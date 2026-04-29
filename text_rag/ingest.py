from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from dotenv import load_dotenv
import os
import logging

logging.getLogger("transformers").setLevel(logging.ERROR)

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data")

if not os.path.exists(DATA_PATH):
    raise Exception(f"Data folder not found: {DATA_PATH}")

pdf_files = [f for f in os.listdir(DATA_PATH) if f.endswith(".pdf")]

if not pdf_files:
    print("No PDF files found in data folder.")
    print("Please add PDF files to text_rag/data/ and run again.")
    raise Exception("No PDF files found. Add files to text_rag/data/")

all_docs = []

for file in pdf_files:
    path = os.path.join(DATA_PATH, file)
    
    loader = PyMuPDFLoader(path)
    docs = loader.load()
    
    for doc in docs:
        doc.metadata["source"] = file
    
    all_docs.extend(docs)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=400,
    chunk_overlap=40
)
chunks = splitter.split_documents(all_docs)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = Chroma.from_documents(
    chunks,
    embedding=embeddings,
    persist_directory=os.path.join(BASE_DIR, "chroma_db")
)