import os
from PyPDF2 import PdfReader

PDF_DIR = r"C:\Users\livei\OneDrive\Escritorio\Rootstrap_Techical\Roostrap_Techical_Assessment\papers"

def load_pdfs():
    texts = []
    metadatas = []

    for file in os.listdir(PDF_DIR):
        if file.endswith(".pdf"):
            path = os.path.join(PDF_DIR, file)
            reader = PdfReader(path)
            full_text = []
            pages = []

            for i, page in enumerate(reader.pages):
                text = page.extract_text()
                if text and text.strip():
                    full_text.append(text)
                    pages.append(i + 1)

            if full_text:
                title = full_text[0].split("\n")[0].strip()
                texts.append("\n".join(full_text))
                metadatas.append({
                    "filename": file,
                    "title": title,
                    "pages": compress_page_ranges(pages)
                })

    return texts, metadatas

def compress_page_ranges(pages):
    if not pages:
        return ""
    pages = sorted(set(pages))
    ranges = []
    start = prev = pages[0]

    for p in pages[1:]:
        if p == prev + 1:
            prev = p
        else:
            ranges.append(f"{start}-{prev}" if start != prev else f"{start}")
            start = prev = p

    ranges.append(f"{start}-{prev}" if start != prev else f"{start}")
    return ",".join(ranges)