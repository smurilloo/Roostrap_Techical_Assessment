
import google.generativeai as genai
import textwrap

genai.configure(api_key="AIzaSyBnzr9P1NSCcF36lXHtf1tA5I9gfIiCcmg")  # Reemplaza con tu API key real

def synthesize_answer(query, pdf_texts, pdf_metadata, memory, web_papers):
    pdf_section = ""
    instruccion_archivos = ""
    if pdf_texts and pdf_metadata:
        pdf_list_text = "\n".join(
            f"- {item['filename']} - {item['title']} (páginas: {item['pages']})"
            for item in pdf_metadata
        )
        pdf_section = f"Fuentes PDF consultadas:\n{pdf_list_text}\n"
        instruccion_archivos = (
            "IMPORTANTE: El modelo no tiene acceso a los archivos originales, "
            "solo al contenido textual proporcionado. Menciona explícitamente las fuentes citadas "
            "usando el formato 'nombre_archivo.pdf - Título del paper (páginas)'."
        )

    web_section = ""
    instruccion_web = ""
    if web_papers:
        web_list_text = "\n".join(
            f"Título: {wp['title']}\nURL: {wp['url']}\nResumen: {wp['snippet']}"
            for wp in sorted(web_papers, key=lambda x: x.get("score", 0), reverse=True)
        )
        web_section = f"Artículos web relevantes desde Google Scholar:\n{web_list_text}\n"
        instruccion_web = (
            "A partir de los artículos web anteriores, redacta dos párrafos con el análisis más relevante, "
            "usando un lenguaje claro y conciso, mencionando explícitamente títulos y URLs."
        )

    documents = "\n\n".join(pdf_texts) if pdf_texts else ""

    prompt = f"""
Contexto previo:
{memory}

Consulta: {query}

Fuentes documentales (texto extraído de PDFs):
{documents}

{pdf_section}
{instruccion_archivos}

{web_section}
{instruccion_web}

Estructura la respuesta iniciando con los hallazgos de los PDFs y luego el análisis de los papers web.
Usa formato claro, con títulos y URLs destacados, viñetas para puntos clave y saltos de línea adecuados.
"""

    model = genai.GenerativeModel("models/gemini-1.5-flash")
    response = model.generate_content(prompt)
    raw_summary = response.text.strip()

    wrapped_summary = "\n".join(textwrap.fill(line, width=80) for line in raw_summary.splitlines())

    return wrapped_summary