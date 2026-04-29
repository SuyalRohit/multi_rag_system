from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from groq import Groq
from dotenv import load_dotenv
import os
import logging

logging.getLogger("transformers").setLevel(logging.ERROR)
load_dotenv()

DEBUG = False
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise Exception("GROQ_API_KEY not found in environment")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

if not os.path.exists(os.path.join(BASE_DIR, "chroma_db")):
    raise Exception(
        "Vector DB not found. Please run 'python text_rag/ingest.py' first."
    )

db = Chroma(
    persist_directory=os.path.join(BASE_DIR, "chroma_db"),
    embedding_function=embeddings
)

client = Groq(api_key=groq_api_key)

def run_text_rag(query):
    docs = db.similarity_search(query, k=3)

    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""
Answer the question based only on the context below.

Context:
{context}

Question:
{query}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    if DEBUG:
        print("Retrieved docs:\n")
        for doc in docs:
            print(doc.page_content[:200])
            print("-----")
    return response.choices[0].message.content