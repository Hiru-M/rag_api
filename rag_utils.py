import pdfplumber
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings


def load_pdf_text(path="transformer.pdf"):
    pages = []
    with pdfplumber.open(path) as pdf:
        for p in pdf.pages:
            pages.append(p.extract_text() or "")
    return "\n".join(pages)


def chunk_text(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=200
    )
    return splitter.split_text(text)


def create_index():
    print("Step 1/3: Loading PDF...")
    text = load_pdf_text("transformer.pdf")

    print("Step 2/3: Splitting text...")
    chunks = chunk_text(text)

    print(f"Created {len(chunks)} chunks.")

    print("Step 3/3: Creating embeddings & saving FAISS...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    vectorstore = FAISS.from_texts(chunks, embedding=embeddings)

    vectorstore.save_local("faiss_index")

    print("✅ FAISS index saved successfully in 'faiss_index/'")


if __name__ == "__main__":
    create_index()
