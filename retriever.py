import os
from PyPDF2 import PdfReader

PDF_DIR = r"C:\Users\livei\OneDrive\Escritorio\Rootstrap_Techical\Roostrap_Techical_Assessment\papers"


def load_pdfs():
    pdfs = []
    metadatas = []

    for file in os.listdir(PDF_DIR):
        if file.endswith(".pdf"):
            path = os.path.join(PDF_DIR, file)
            reader = PdfReader(path)
            pages_texts = []
            pages_numbers = []

            for i, page in enumerate(reader.pages):
                text = page.extract_text()
                if text and text.strip():
                    pages_texts.append({"page": i+1, "text": text.strip()})
                    pages_numbers.append(i+1)

            if pages_texts:
                title = pages_texts[0]['text'].split("\n")[0].strip()
                pdfs.append({
                    "filename": file,
                    "title": title,
                    "pages_texts": pages_texts
                })
                metadatas.append({
                    "filename": file,
                    "title": title,
                    "pages": compress_page_ranges(pages_numbers)
                })

    return pdfs, metadatas



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