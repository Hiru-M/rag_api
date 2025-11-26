# RAG Transformer Paper API

This is a small project for my internship assignment.  
It lets you ask questions about the “Attention Is All You Need” Transformer paper.

The system works like this:
- The PDF is split into text chunks.
- A FAISS index is created using sentence-transformer embeddings.
- When you ask a question, the most relevant chunks are retrieved.
- The answer is generated using a free model from OpenRouter.
- The backend is built using FastAPI.
- A simple Streamlit UI is included.

## How to Run the Project

### 1. Create the FAISS index (run once)
### 2. Start the FastAPI server
API will be available at:http://127.0.0.1:8000/docs
### 3. Start the Streamlit UI

## Environment Variables
Create a file named `.env` and add your OpenRouter key:

## Docker

To build the Docker container:

To run it:docker run -p 8000:8000 rag-transformer-api

## Files

- **app/main.py** — FastAPI backend  
- **scripts/build_index.py** — creates FAISS index  
- **app_streamlit.py** — simple UI  
- **requirements.txt** — dependencies  
- **Dockerfile** — container setup  


