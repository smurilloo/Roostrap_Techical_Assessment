from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from memory_keeper import MemoryKeeper
from retriever import load_pdfs
from synthesizer import synthesize_answer
from web_searcher import get_web_papers_selenium

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

memory_keeper = MemoryKeeper()

@app.get("/", response_class=HTMLResponse)
async def root():
    html_path = Path(__file__).parent / "static" / "index.html"
    with open(html_path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.post("/ask")
async def ask(request: Request):
    data = await request.json()
    question = data.get("question", "").strip()

    if not question:
        return JSONResponse(content={"answer": "Por favor ingresa una consulta válida."}, status_code=400)

    try:
        pdf_texts, pdf_metadata = load_pdfs()

        web_papers = get_web_papers_selenium(question)

        memory = memory_keeper.get_context()

        answer = synthesize_answer(question, pdf_texts, pdf_metadata, memory, web_papers)

        memory_keeper.remember(question, answer)

        return JSONResponse(content={"answer": answer})

    except Exception as e:
        return JSONResponse(content={"answer": f"Error procesando la consulta: {str(e)}"}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
