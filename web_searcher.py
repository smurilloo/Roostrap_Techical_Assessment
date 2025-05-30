import google.generativeai as genai
from typing import List, Dict
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import textwrap

genai.configure(api_key="AIzaSyD4DG2T5KlFUK9ohBzsO4Jf99uye_7XXJE")  # ← reemplaza por tu propia API key

def get_web_papers_selenium(query: str, max_pages: int = 10) -> List[Dict]:
    base_url = "https://scholar.google.com/scholar"
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    results = []
    for page in range(max_pages):
        start = page * 10
        search_url = f"{base_url}?q={query.replace(' ', '+')}&start={start}"
        driver.get(search_url)
        time.sleep(3)

        articles = driver.find_elements(By.CSS_SELECTOR, "div.gs_ri")
        for art in articles:
            try:
                title_elem = art.find_element(By.CSS_SELECTOR, "h3 a")
                title = title_elem.text.strip()
                url = title_elem.get_attribute("href")
                snippet_elem = art.find_elements(By.CLASS_NAME, "gs_rs")
                snippet = snippet_elem[0].text.strip() if snippet_elem else "No hay resumen disponible."
                results.append({"title": title, "url": url, "snippet": snippet})
            except Exception:
                continue

    driver.quit()
    return results

def get_annotated_summary(query: str) -> str:
    papers = get_web_papers_selenium(query)
    if not papers:
        return "No se encontraron artículos."

    prompt = "".join(
        f"Título: {p['title']}\nResumen: {p['snippet']}\nURL: {p['url']}\n\n" for p in papers
    )

    full_prompt = f"""
Analiza los siguientes artículos científicos obtenidos de Google Scholar y genera un resumen claro y estructurado en formato tipo documento. Por favor:

- Usa dos párrafos separados.
- Incorpora títulos y URLs destacados en líneas propias.
- Usa viñetas o numeración para temas comunes o puntos importantes.
- Añade saltos de línea para facilitar la lectura.
- No dejes líneas con más de 80 caracteres; usa saltos de línea para ajustar el texto.

Aquí están los artículos a analizar:

{prompt}
"""

    model = genai.GenerativeModel("models/gemini-1.5-flash")
    response = model.generate_content(full_prompt)
    raw_summary = response.text.strip()

    # Aplicar wrap para evitar líneas muy largas, respetando saltos de línea originales
    wrapped_summary = "\n".join(textwrap.fill(line, width=80) for line in raw_summary.splitlines())

    return wrapped_summary