# app/main.py

from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv

from openai import OpenAI
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

load_dotenv()

app = FastAPI()

class Question(BaseModel):
    question: str


# ---------------------------
# Load embeddings + vector store
# ---------------------------
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

vectorstore = FAISS.load_local(
    "faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})


# ---------------------------
# OpenRouter Client
# ---------------------------
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.3"


def generate_answer(question: str, context: str):
    prompt = f"""
Use the context below to answer the question clearly and simply.

Context:
{context}

Question:
{question}

Answer:
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    return response.choices[0].message.content


# ---------------------------
# FastAPI Route
# ---------------------------
@app.post("/ask")
def ask(q: Question):
    docs = retriever.invoke(q.question)
    context = "\n\n".join([d.page_content for d in docs])

    answer = generate_answer(q.question, context)

    return {
        "question": q.question,
        "answer": answer,
        "context": context
    }
