# Phase 3: Document Processing

## Overview
Phase 3 focuses on preparing raw documents for a (RAG) pipeline.
The objective of this phase is to extract **text and images from PDF documents**, split the text into manageable chunks, and generate structured metadata that links text chunks with relevant images.

This phase acts as the **data preparation layer** for later stages such as embedding generation and vector database ingestion.

---

## Objectives
The main objectives of Phase 3 are:

- Parse PDF documents and extract textual content
- Extract embedded images from PDF pages
- Split long text into overlapping chunks suitable for embedding models
- Generate metadata linking text chunks with images and source information
- Produce structured outputs for downstream multimodal processing

---

## Tools and Libraries Used

| Tool / Library | Purpose |
|----------------|--------|
| PyMuPDF (fitz) | PDF parsing, text extraction, and image extraction |
| Pillow         | Image handling support |
| Python Standard Library | File handling and JSON generation |

All dependencies are managed inside a Python virtual environment to ensure isolation and reproducibility.

---

## Project Structure
src/
├── phase3_main.py
├── document_processor.py
├── chunking.py

data/
└── pdfs/
└── sample_document.pdf

output/
├── images/
└── metadata.json

- `document_processor.py` handles PDF parsing and image extraction
- `chunking.py` contains the text chunking logic
- `phase3_main.py` orchestrates the full Phase 3 pipeline

---

## Text Chunking Strategy
Text extracted from PDFs may exceed the input limits of embedding models.
To address this, a **fixed-size chunking strategy with overlap** is used.

- Chunk size: approximately 300 words
- Overlap: 40 words
- Overlapping chunks help preserve contextual continuity across segments
---

## Metadata Generation and Image Linking
For each text chunk, metadata is generated containing:

- Unique chunk identifier
- Page number
- Text content
- References to images extracted from the same page
- Source document information

Images are linked to text chunks based on page-level association

## Output of Phase 3
At the end of Phase 3, the pipeline produces:

- A folder containing extracted images
- A structured `metadata.json` file containing:
  - Text chunks
  - Image references
  - Page and source metadata


