import fitz  # PyMuPDF
import os

def process_pdf(pdf_path, image_output_dir):
    doc = fitz.open(pdf_path)
    pages_data = []

    os.makedirs(image_output_dir, exist_ok=True)

    for page_index in range(len(doc)):
        page = doc[page_index]

        # Extract text
        text = page.get_text()

        # Extract images
        images = []
        for i, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)

            image_name = f"page_{page_index}_img_{i}.png"
            image_path = os.path.join(image_output_dir, image_name)
            pix.save(image_path)

            images.append(image_name)

        pages_data.append({
            "page": page_index,
            "text": text,
            "images": images
        })

    return pages_data
