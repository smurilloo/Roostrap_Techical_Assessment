from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import re
import google.generativeai as genai

genai.configure(api_key="AIzaSyD4DG2T5KlFUK9ohBzsO4Jf99uye_7XXJE")

def get_top_news_selenium(url, max_news=10):
    options = Options()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    time.sleep(5)
    articles = driver.find_elements(By.XPATH, '//a[contains(@href, "/news/") and string-length(text()) > 20]')
    seen, results = set(), []
    for a in articles:
        href = a.get_attribute("href")
        text = a.text.strip()
        if href and text and href not in seen:
            results.append({'title': text, 'url': href})
            seen.add(href)
        if len(results) >= max_news:
            break
    driver.quit()
    return results

def summarize_and_score_sentiment(text):
    prompt = f"""
Resumen de noticias:
{text}
"""
    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip()