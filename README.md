# AI Command Center

AI Command Center is a unified platform housing **five distinct, highly-specialized AI personas**, each engineered for specific academic and professional tasks. Rather than providing a single generic chatbot with different system prompts, each persona in this platform features tailored prompt designs, behavioral rules, structured output schemas, and specific data retrieval pipelines.

## 🚀 The Problem It Solves

Generic AI chatbots often fail when tasked with specialized workflows—they hallucinate answers on documents, give away the full answer when you're trying to learn a concept, or provide unformatted blocks of text for code reviews. 

AI Command Center solves this by providing:
1. **Targeted Workflows:** Distinct tools designed for specific use-cases (e.g., Code Reviewer generates structured tables; Study Mentor asks questions instead of just giving answers).
2. **Reliability & Fallbacks:** A robust backend that intelligently routes between Gemini and Mistral based on the task, and automatically falls back to Groq if the primary provider hits a rate limit or goes down.
3. **No Hallucinations on Docs:** A custom Document Analyzer that uses strict keyword-based chunk retrieval (no vector RAG) to ensure it only answers from the text provided.

## 🤖 The 5 Personas

1. **Study Mentor:** Acts as a tutor. It breaks concepts down, checks your understanding, and re-explains if you're confused. It will *not* just dump the answer.
2. **Code Reviewer:** Analyzes code and outputs structured JSON (rendered as neat UI sections) covering Bugs, Security Vulnerabilities, Performance, and Style/Best Practices, along with suggested fixes.
3. **Code Colleague:** A pair-programming assistant that helps you write, debug, and architect software.
4. **Document Analyzer:** Upload a PDF and ask questions. It strictly grounds its answers in the document using a custom text-chunking and keyword-scoring algorithm. If the answer isn't there, it explicitly says so.
5. **Resume Reviewer:** Analyzes resumes and provides structured, actionable feedback (Strengths, Gaps, and concrete Before/After rewrite suggestions).

## 🛠️ Technology Stack & Languages

The project is designed to be lightweight, performant, and deployable as a single containerized application.

### Languages Used (Approximate)
- **Python (60%):** Drives the powerful FastAPI backend, LLM routing logic, PDF parsing, and keyword retrieval logic.
- **JavaScript (25%):** Powers the dynamic Vanilla JS frontend (Server-Sent Events streaming, Markdown rendering, File uploading, and UI interactions).
- **CSS (10%):** A custom, bespoke dark-theme stylesheet (`styles.css`) for a premium "Elite Terminal" feel.
- **HTML (5%):** Clean, semantic HTML5 structure for the frontend shell.

### Frameworks & Tools
- **Backend:** FastAPI, Uvicorn, Pydantic
- **Frontend:** Vanilla JS, Marked.js (Markdown parsing), Highlight.js (Code highlighting)
- **Document Parsing:** PyPDF

## 🧠 LLMs Used (The Routing Engine)

The system utilizes an intelligent LLM routing engine that picks the best model for the job:

1. **Google Gemini (`gemini-2.5-flash`):** Primary engine for *Study Mentor, Document Analyzer, Resume Reviewer*, and *Research Assistant*. Also handles text embeddings.
2. **Mistral (`codestral-latest`):** Primary engine for code-heavy tasks (*Code Reviewer* and *Code Colleague*) due to its specialized training on code generation.
3. **Groq (`llama-3.3-70b-versatile`):** Acts as the **Global Fallback**. If Gemini or Mistral fail due to rate limits or API outages, the backend seamlessly catches the error and streams the response via Groq without interrupting the user experience.

## 📖 Complete Setup & Usage Guide

### Prerequisites
- Python 3.10+
- Git

### 1. Installation

Clone the repository and navigate into the backend folder:
```bash
git clone https://github.com/Ysaibhanu99/AI_COMMAND_CENTER.git
cd AI_COMMAND_CENTER/backend
```

Create a virtual environment and install the dependencies:
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Configuration

Copy the example environment file and add your API keys:
```bash
cp .env.example .env
```
Open `.env` and fill in your API keys:
- `GEMINI_API_KEY` (Get from Google AI Studio)
- `MISTRAL_API_KEY` (Get from Mistral AI Platform)
- `GROQ_API_KEY` (Get from GroqConsole)

### 3. Running the Server

Start the FastAPI server using Uvicorn:
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

### 4. How to Use It
1. Open your browser and navigate to **[http://localhost:8080](http://localhost:8080)**.
2. You will be greeted by the Dashboard. Click on any of the **Persona Cards** to enter that specific workspace.
3. **For Chat Personas (Study Mentor, Code Colleague):** Simply start typing your queries in the terminal input at the bottom.
4. **For Document Personas (Document Analyzer, Resume Reviewer):** Use the drag-and-drop upload zone at the top of the workspace to attach a PDF before asking your questions.
5. Watch the AI stream its response back in real-time!

## ⚙️ How It Actually Works (Under the Hood)

1. **Unified Routing:** When the frontend sends a chat message, it POSTs to `/api/chat/{persona_id}`. 
2. **Persona Registry:** The backend looks up the specific `PersonaConfig` for that ID. This config dictates the system prompt, the required input format (e.g., requires upload), and whether the output should be freeform Markdown or strictly constrained JSON schema.
3. **LLM Orchestrator:** The `call_llm_stream` function checks which model is the "primary" for that persona (Mistral vs Gemini). It opens a streaming connection. 
4. **Server-Sent Events (SSE):** As chunks of text are generated by the LLM, the backend yields them immediately to the frontend using an async generator, creating a fast, real-time typing effect.
5. **Structured Parsing:** For Personas like Code Reviewer, the LLM outputs strict JSON. The frontend (`structured.js`) catches this JSON, parses it, and injects it into a beautiful custom UI with separate cards for Bugs, Security, and Style, complete with code-diff blocks.
