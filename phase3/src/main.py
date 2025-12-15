import os
import json
from document_processor import process_pdf
from chunking import chunk_text

os.makedirs("output", exist_ok=True)

PDF_PATH = 'D:/4/Intern/Projects/phase3/data/transformer.pdf'
IMAGE_OUTPUT_DIR = 'D:/4/Intern/Projects/phase3/output/images'
METADATA_OUTPUT = 'D:/4/Intern/Projects/phase3/output/metadata.json'

all_chunks_metadata = []
pages = process_pdf(PDF_PATH, IMAGE_OUTPUT_DIR)

for page_data in pages:
    page_number = page_data["page"]
    text = page_data["text"]
    images = page_data["images"]

    chunks = chunk_text(text)

    for i, chunk in enumerate(chunks):
        all_chunks_metadata.append({
            "chunk_id": f"p{page_number}_c{i}",
            "page": page_number,
            "text": chunk,
            "linked_images": images,
            "source_pdf": PDF_PATH
        })

with open(METADATA_OUTPUT, "w", encoding="utf-8") as f:
    json.dump(all_chunks_metadata, f, indent=2)

print(f"Phase-3 completed. Generated {len(all_chunks_metadata)} chunks.")
