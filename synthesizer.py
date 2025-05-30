import google.generativeai as genai

genai.configure(api_key="AIzaSyD4DG2T5KlFUK9ohBzsO4Jf99uye_7XXJE")

def synthesize_answer(query, documents, web_info, memory, pdf_files=None):
    if pdf_files:
        pdf_list_text = "\n".join(
            f"- {item['filename']} - {item['title']} (páginas: {item['pages']})"
            for item in pdf_files
        )
        pdf_section = f"Fuentes PDF consultadas:\n{pdf_list_text}\n"
        instruccion_archivos = (
            "IMPORTANTE: El modelo no tiene acceso a los archivos originales, "
            "solo al contenido textual proporcionado. Menciona explícitamente las fuentes citadas "
            "usando el formato 'nombre_archivo.pdf - Título del paper (páginas)'."
        )
    else:
        pdf_section = ""
        instruccion_archivos = ""

    prompt = f"""
Contexto previo:
{memory}

Consulta: {query}

Fuentes documentales (texto extraído de PDFs):
{documents}

Fuentes web:
{web_info}

{pdf_section}
{instruccion_archivos}

Responde con explicaciones claras y referencias explícitas a las fuentes usando el formato indicado.
"""
    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip()
