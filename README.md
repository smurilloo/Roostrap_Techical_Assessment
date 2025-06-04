# 🧪 **Neuroscience Foundation Q&A Crew**

**IMPORTANT**: The code must be developed using **Python** and shared on **Github**.

## 📚 **Case Scenario**
You’ve been hired to prototype an intelligent assistant for a neuroscience foundation. This assistant should help researchers, students, and curious minds answer questions about dopamine, pulling from both **internal research papers** and **external trusted sources on the web**.
To accomplish this, you will design a multi-agent system ("the crew") powered by Large Language Models (LLMs). This crew should collaborate to **retrieve, analyze, and synthesize** information from 10 provided research papers PDFs and supplement answers with reliable web-based sources if needed. Importantly, your crew should be able to **remember** the conversation context to support follow-up questions.

## 🧠 **Objective:**
Create a multi-agent system capable of answering questions about **dopamine** by performing:

* **RAG** (Retrieval-Augmented Generation) using 10 PDF documents
* **Live web search** to fill in gaps or verify claims
* **Source-aware generation**: Each answer should clearly state where the information came from (e.g., “Paper X, page 5”, or “NIH.gov”)
* **Conversational memory**: Maintain useful dialogue context across a session

## 📦 **Resources Provided:**
* A set of 10 neuroscience-focused research PDFs about dopamine

## ✅ **What We Expect From You**
**Required Features:**
* 🧑‍🤝‍🧑 A **modular crew** of agents (e.g., Retriever, Synthesizer, WebSearcher, Memory Keeper)
* 🧾 Responses that include **source citations** (PDF metadata or web URLs)
* 🧠 A functioning **memory system** that allows contextual follow-up questions
* 🔄 A simple **interface** to interact with the crew

**Extra Points Bonus Features:**
* 🗺️ **Diagram + explanation** of your agent architecture
* 📊 Structured response output (e.g., JSON with answer, sources, and reasoning steps)
* 🕵️‍♂️ Handling ambiguous or controversial dopamine topics by flagging or explaining uncertainty
* 🧱 **Optional Deployment Architecture**:
	* A document describing how you'd deploy this crew
	* Include infrastructure considerations (memory, scalability, cost)

## 🧪 **Sample Questions You Might Want to Test**
*These don’t need to be hardcoded — just useful for your testing.*
* What is dopamine and what role does it play in motivation?
* How does dopamine influence learning and reward processing?
* Are dopamine detox strategies backed by science?
* How is dopamine involved in addiction vs habit formation?
* Can you summarize differences in dopamine function between ADHD and Parkinson's disease?

## 📁 **Expected Output**
**Github repo including:**
* **Readme** with **decisions made**, **instructions**, and/or any additional comments you wish to make
* **Code developed** to solve the Challenge

## **Good Luck!**




🎯 Funcionalidades Principales
✅ Búsqueda y recuperación desde documentos PDF
✅ Búsqueda web confiable y resumen automático
✅ Generación con citas claras de fuentes
✅ Memoria contextual para preguntas encadenadas
✅ Interfaz web simple con FastAPI

📦 Instalación y Ejecución Local
Clona este repositorio

bash
Copy
Edit
git clone <url-del-repo>
cd <repo>
Crea un entorno virtual

bash
Copy
Edit
python -m venv venv
Actívalo

bash
Copy
Edit
# Windows
venv\Scripts\activate
Instala dependencias

bash
Copy
Edit
pip install -r requirements.txt
Ejecuta la API con FastAPI

bash
Copy
Edit
python -m uvicorn main:app --reload

Abre en navegador:

cpp
Copy
Edit
http://127.0.0.1:8000

🧠 Componentes Técnicos
retriever.py
Carga y vectoriza los documentos PDF usando PyPDF2 y FAISS. Extrae texto por página y lo acompaña con metadatos como nombre del archivo y número de página.

web_searcher.py
Utiliza Selenium para scrapear las últimas noticias desde sitios como NIH.gov y luego resume con Gemini 1.5 de Google. Puede ampliarse fácilmente a otros dominios.

memory_keeper.py
Sistema de memoria simple basado en listas, almacena contexto de preguntas/respuestas y lo entrega como entrada al generador.

synthesizer.py
Modelo generativo (Gemini) que compone una respuesta final combinando:

Documentos PDF relevantes

Resultados de búsqueda web

Memoria conversacional

main.py
Controlador de endpoints FastAPI. Coordina todos los módulos del crew y devuelve la respuesta al usuario.

static/index.html
Interfaz web muy sencilla con entrada de texto y botón para enviar preguntas al backend.

🔍 Ejemplos de Preguntas Útiles

* What is dopamine and what role does it play in motivation?
* How does dopamine influence learning and reward processing?
* Are dopamine detox strategies backed by science?
* How is dopamine involved in addiction vs habit formation?
* Can you summarize differences in dopamine function between ADHD and Parkinson's disease?

📂 Estructura del Repositorio
cpp
Copy
Edit
.
├── main.py
├── retriever.py
├── synthesizer.py
├── web_searcher.py
├── memory_keeper.py
├── static/
│   └── index.html
├── requirements.txt
├── README.md
└── papers/
    └── (10 archivos PDF)

✅ Funcionalidades Extras Incluidas
🔗 Citas explícitas por fuente documental y web

💬 Retención contextual para preguntas consecutivas

🔍 Indicadores de incertidumbre en temas debatidos

📊 Preparado para extender a respuestas estructuradas JSON



🧪 Requisitos Técnicos
Python 3.11

FastAPI

LangChain

HuggingFace Transformers

FAISS

PyPDF2

Selenium

Google Generative AI SDK

🙌 Créditos
Desarrollado por [Samuel Murillo Ospina], 2025
Challenge técnico para Rootstrap: Neuro Assistant AI