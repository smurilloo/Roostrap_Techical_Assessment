from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from retriever import load_pdfs
from web_searcher import get_top_news_selenium, summarize_and_score_sentiment
from synthesizer import synthesize_answer
from memory_keeper import MemoryKeeper

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

memory = MemoryKeeper()
texts, metadatas = load_pdfs()

@app.get("/", response_class=HTMLResponse)
def root():
    with open("static/index.html") as f:
        return f.read()

@app.post("/ask")
async def ask(request: Request):
    data = await request.json()
    query = data['question']
    
    web_results = get_top_news_selenium("https://www.nih.gov/news-events/news-releases")
    summary = summarize_and_score_sentiment("\n".join([n['title'] for n in web_results]))

    docs_subset = texts[:10]
    metadata_subset = metadatas[:10]
    documents = "\n".join(docs_subset)
    context = memory.get_context()

    # Construir lista detallada de archivos consultados
    pdf_files_consulted = []
    for md in metadata_subset:
        filename = md.get("filename", "archivo_desconocido.pdf")
        title = md.get("title", "Título no disponible")
        pages = md.get("pages", "páginas no especificadas")
        pdf_files_consulted.append({
            "filename": filename,
            "title": title,
            "pages": pages
        })

    answer = synthesize_answer(query, documents, summary, context, pdf_files=pdf_files_consulted)
    memory.remember(query, answer)
    return JSONResponse({"answer": answer})
