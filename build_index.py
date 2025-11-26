import sys
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from app.rag_utils import load_pdf_text, chunk_text
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

text = load_pdf_text("transformer.pdf")
chunks = chunk_text(text)

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

vectorstore = FAISS.from_texts(chunks, embeddings)
vectorstore.save_local("faiss_index")

print("✅ Index created successfully.")
