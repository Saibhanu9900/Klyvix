# 🎯 Klyvix

<p align="center">
  <img src="klyvix-logo.png" alt="Klyvix Logo" width="200">
</p>

> A **unified, high-performance platform** housing **6 specialized AI personas**, each engineered for specific academic and professional workflows. Powered by intelligent multi-LLM routing with real-time streaming.

---

## 🚀 What It Solves

Generic AI chatbots fail when tasked with specialized workflows:
- ❌ They hallucinate answers on documents
- ❌ They dump full answers when you're trying to learn
- ❌ They output unformatted walls of text
- ❌ They lack domain-specific expertise

**Klyvix** fixes this by providing:

| Challenge | Solution |
|-----------|----------|
| **Generic AI responses** | 6 purpose-built personas, each fine-tuned for specific workflows |
| **Document hallucinations** | Semantic vector retrieval via Qdrant + Gemini embeddings — answers strictly grounded in your documents |
| **Rate limits & outages** | Intelligent LLM fallback engine — routes between Gemini, Mistral, and Groq seamlessly |
| **Unstructured outputs** | Structured JSON for code reviews & resume feedback + formatted markdown for interactive learning |
| **Slow interactions** | Real-time Server-Sent Events (SSE) streaming with terminal-style UI |

---

## 🤖 The 6 AI Personas

### 1. **📚 Study Mentor**
Your personal Socratic tutor with two modes:
- **Direct Mode:** Comprehensive, structured answers with LaTeX math, tables, and examples (exam-ready)
- **Socratic Mode:** Interactive learning with questions that check your understanding

**Use for:** Learning complex concepts, exam prep, step-by-step problem solving

---

### 2. **🔍 Code Reviewer**
Systematic code audit across 4 critical dimensions:
- **Bugs & Correctness** — Logic errors, off-by-one mistakes, null pointer risks
- **Security** — Input validation, injection risks, hardcoded secrets
- **Performance** — Inefficient loops, unnecessary allocations, algorithmic complexity
- **Style & Best Practices** — Naming, organization, language idioms

Outputs structured JSON rendered as a beautiful multi-section UI card.

**Use for:** Code quality assurance, security hardening, performance optimization

---

### 3. **👥 Code Colleague**
A collaborative pair-programming partner:
- Writes complete, production-ready code (never pseudocode)
- Asks clarifying questions when requirements are ambiguous
- Explains design decisions and trade-offs
- Suggests improvements and alternatives
- Supports rapid iterative refinement

**Use for:** Code generation, debugging, architecture design, refactoring

---

### 4. **📄 Document Analyzer**
Upload a PDF and ask anything. Guaranteed ground-truth answers:
- Extracts answers **strictly from your document** using semantic vector retrieval (Qdrant + Gemini embeddings)
- Cites exact sections/chunks
- Refuses to guess or hallucinate
- Handles multi-document context

**Use for:** Research papers, contracts, reports, PDFs, compliance documents

---

### 5. **📋 Resume Reviewer**
Professional resume optimization with actionable feedback:
- **Strengths:** Identifies what's working (quantified achievements, clarity)
- **Gaps:** Flags vague language, missing metrics, formatting issues
- **Suggestions:** Shows before/after rewrites with explanations of why changes matter

Outputs structured feedback as beautiful cards.

**Use for:** Job application prep, career transitions, LinkedIn optimization

---

### 6. **🔬 Research Assistant**
Web-powered research analyst with Google Search grounding:
- Actively searches the web for current, real-time information
- Cites sources with links
- Flags where sources agree vs. conflict
- Organizes by theme (not source-by-source)
- Identifies gaps and limitations

**Use for:** Literature reviews, competitive analysis, trend synthesis, evidence-based research

---

## 🏗️ Architecture at a Glance

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (Vanilla JS)                     │
│  • Server-Sent Events (SSE) streaming                        │
│  • Real-time markdown rendering + code highlighting          │
│  • Structured UI card rendering for JSON outputs             │
│  • Drag-and-drop file uploads                                │
└──────────────────────┬──────────────────────────────────────┘
                       │ /api/chat/{persona_id}
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              FastAPI Backend (Python)                        │
│  • Persona Registry: 6 specialized system prompts             │
│  • Multi-LLM Router: Routes to Gemini, Mistral, or Groq      │
│  • Document Processing: PDF parsing + semantic chunking      │
│  • Vector Retrieval: Qdrant with Gemini embeddings (768-dim) │
│  • Auth: JWT tokens with bcrypt password hashing             │
│  • Redis: Rate limiting + LLM response caching              │
└──────────┬───────────┬───────────┬──────────────────────────┘
           │           │           │
    ┌──────┴──┐  ┌─────┴────┐  ┌──┴─────┐
    │ Gemini  │  │ Mistral  │  │  Groq  │
    │(Primary)│  │ (Code)   │  │(Fallback)│
    └─────────┘  └──────────┘  └────────┘
      • Study Mentor      • Code Reviewer
      • Doc Analyzer      • Code Colleague
      • Resume Reviewer
      • Research Assistant

    ┌──────────┐  ┌─────────┐  ┌───────┐
    │PostgreSQL│  │ Qdrant  │  │ Redis │
    │(Neon)│  │ (Cloud) │  │(Upstash)│
    └──────────┘  └─────────┘  └───────┘
      • Users           • Document       • Rate limiting
      • Documents         embeddings     • LLM response
      • Chat sessions   • 768-dim          caching
                          vectors
```

---

## ⚡ Tech Stack

| Layer | Technology |
|-------|-----------:|
| **Backend** | Python 3.12, FastAPI, Uvicorn, Pydantic |
| **Frontend** | Vanilla JS (ES6+), Marked.js, Highlight.js, KaTeX |
| **LLM Providers** | Google Gemini 2.0 Flash, Mistral Codestral, Groq Llama 3.3 70B |
| **Vector Store** | Qdrant Cloud (768-dim Gemini embeddings, cosine similarity) |
| **Database** | PostgreSQL (Neon) — users, documents, chat sessions |
| **Cache** | Redis (Upstash) — rate limiting, LLM response caching |
| **Auth** | JWT tokens, bcrypt password hashing (passlib) |
| **Deployment** | Render (render.yaml), Docker |
| **Streaming** | Server-Sent Events (SSE) for real-time responses |

**Language Breakdown:**
- 🐍 **Python (43.7%)** — FastAPI backend, LLM routing, PDF parsing
- 🟨 **JavaScript (30.5%)** — Dynamic frontend, SSE streaming, UI interactions
- 🎨 **CSS (19.6%)** — Premium dark-theme "Elite Terminal" styling
- 📝 **HTML (5.9%)** — Semantic HTML5 structure
- 🐳 **Dockerfile (0.3%)** — Container configuration

---

## 📖 Quick Start

### Prerequisites
- Python 3.10+
- Git
- PostgreSQL (or a [Neon](https://neon.tech) free tier account)
- Qdrant (or a [Qdrant Cloud](https://cloud.qdrant.io) free tier account)
- Redis (or an [Upstash](https://upstash.com) free tier account)

### 1️⃣ Clone & Setup

```bash
git clone https://github.com/Ysaibhanu99/Klyvix.git
cd Klyvix/backend

# Create virtual environment
python -m venv venv

# Activate (macOS/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Configure Environment

```bash
cp .env.example .env
```

Open `.env` and fill in **all** required values:

```env
# API Keys
GEMINI_API_KEY=your_key_here         # Get from Google AI Studio
MISTRAL_API_KEY=your_key_here        # Get from Mistral AI
GROQ_API_KEY=your_key_here           # Get from Groq Console

# Database & Infrastructure
DATABASE_URL=postgresql://...        # Neon connection string
QDRANT_URL=https://...               # Qdrant Cloud cluster URL
QDRANT_API_KEY=your_key_here         # Qdrant API key
REDIS_URL=redis://...                # Upstash Redis URL
JWT_SECRET_KEY=your_secret_here      # Generate: python -c "import secrets; print(secrets.token_hex(32))"
```

**Get API Keys:**
- 🔵 [Google Gemini](https://aistudio.google.com/app/apikey)
- 🟦 [Mistral AI](https://console.mistral.ai/api-keys/)
- ⚡ [Groq](https://console.groq.com)

**Get Infrastructure:**
- 🐘 [Neon](https://neon.tech) — Free PostgreSQL
- 🔷 [Qdrant Cloud](https://cloud.qdrant.io) — Free vector DB (1GB)
- 🔴 [Upstash](https://upstash.com) — Free Redis

### 4️⃣ Run Server

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

### 5️⃣ Open in Browser

Navigate to: **[http://localhost:8080](http://localhost:8080)**

✨ You should see the dashboard with 6 persona cards!

---

## 🎮 How to Use

### Dashboard
Click any **persona card** to enter that workspace

### Chat Personas (Study Mentor, Code Colleague, Research Assistant)
1. Type your query in the terminal input at the bottom
2. Watch real-time streaming responses
3. Maintain conversation history automatically

### Document Personas (Analyzer, Resume Reviewer)
1. **Drag-and-drop** a PDF into the upload zone, OR
2. Click the **[+]** icon to select files
3. Ask your questions — answers are grounded in the document via semantic vector retrieval

### Structured Output (Code Reviewer, Resume Reviewer)
Responses render as beautiful multi-section cards with:
- Color-coded severity levels
- Expandable sections (Bugs, Security, Performance, etc.)
- Before/after comparisons
- Copy-to-clipboard code snippets

---

## 🔧 How It Works Under the Hood

### Request Flow

1. **Frontend** sends a message to `/api/chat/{persona_id}` with streaming enabled
2. **Persona Lookup** retrieves the specialized system prompt and configuration
3. **Document Retrieval** (if needed) — semantic vector search finds relevant chunks from uploaded PDFs via Qdrant
4. **LLM Routing** — selects primary provider (Gemini for study/docs, Mistral for code, Groq as fallback)
5. **Streaming** — backend streams tokens in real-time via SSE
6. **Frontend** renders tokens as they arrive, handling markdown/JSON/KaTeX formatting
7. **Structured Parsing** (for JSON outputs) — renders as interactive UI cards

### Intelligent Fallback
If the primary provider fails:
- 🚨 **Primary fails** → Logs the error
- 🔄 **Groq fallback activates** → Continues the stream seamlessly
- 📝 **Partial responses** → If tokens were already sent, instructs fallback to continue naturally

### Caching
- LLM responses are cached in Redis (24hr TTL) keyed by SHA-256 hash of the prompt inputs
- Duplicate uploads are detected by file hash and return cached metadata instantly

---

## 📦 Deployment

### Render (Recommended)

The `render.yaml` in the project root configures a Render web service. Add your environment variables in the Render dashboard and connect your GitHub repo.

### Docker

```bash
# Build image
docker build -t klyvix .

# Run container
docker run -p 8080:8080 \
  -e GEMINI_API_KEY=your_key \
  -e MISTRAL_API_KEY=your_key \
  -e GROQ_API_KEY=your_key \
  -e DATABASE_URL=your_db_url \
  -e QDRANT_URL=your_qdrant_url \
  -e QDRANT_API_KEY=your_qdrant_key \
  -e REDIS_URL=your_redis_url \
  -e JWT_SECRET_KEY=your_secret \
  klyvix
```

### Environment Variables

| Variable | Required | Source |
|----------|----------|--------|
| `GEMINI_API_KEY` | Yes | Google AI Studio |
| `MISTRAL_API_KEY` | Yes | Mistral AI Console |
| `GROQ_API_KEY` | Yes | Groq Console |
| `DATABASE_URL` | Yes | Neon / PostgreSQL |
| `QDRANT_URL` | Yes | Qdrant Cloud |
| `QDRANT_API_KEY` | Yes | Qdrant Cloud |
| `REDIS_URL` | Yes | Upstash / Redis |
| `JWT_SECRET_KEY` | Yes | Self-generated (see .env.example) |
| `HOST` | No | Default: `0.0.0.0` |
| `PORT` | No | Default: `8080` |
| `CORS_ORIGINS` | No | Default: `["*"]` |

---

## 📂 Project Structure

```
Klyvix/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI app entry point (lifespan handler)
│   │   ├── core/
│   │   │   ├── llm_client.py       # Multi-LLM routing + streaming + caching
│   │   │   ├── retrieval.py        # PDF parsing, chunking, Qdrant vector storage & search
│   │   │   ├── config.py           # Settings & environment (pydantic-settings)
│   │   │   ├── auth.py             # JWT tokens, bcrypt password hashing, guest access
│   │   │   ├── cache.py            # Redis cache (Upstash) for rate limiting & LLM responses
│   │   │   ├── rate_limit.py       # Per-IP rate limiting via Redis
│   │   │   └── logger.py           # Structured JSON logging (structlog)
│   │   ├── personas/
│   │   │   └── registry.py         # 6 persona configs, prompts & temperature settings
│   │   ├── routers/
│   │   │   ├── chat.py             # Chat streaming endpoint (SSE)
│   │   │   ├── upload.py           # File upload endpoint (PDF processing)
│   │   │   └── auth.py             # Register, login & guest access endpoints
│   │   └── models/
│   │       ├── schemas.py          # Pydantic models (request/response)
│   │       └── database.py         # SQLAlchemy models (User, Document, ChatSession)
│   ├── tests/
│   │   ├── test_api.py             # API endpoint tests
│   │   └── test_retrieval.py       # Chunking & retrieval tests
│   ├── static/
│   │   ├── index.html              # Frontend shell
│   │   ├── css/styles.css          # Dark-theme "Elite Terminal" styling
│   │   └── js/
│   │       ├── app.js              # Main app logic & persona management
│   │       ├── api.js              # API client with JWT auth
│   │       └── components/         # Chat, structured output, upload components
│   ├── requirements.txt            # Python dependencies
│   └── .env.example                # Environment template (all required vars)
├── Dockerfile                      # Docker configuration
├── render.yaml                     # Render deployment config
└── README.md                       # This file
```

---

## 🛠️ Development

### Add a New Persona

1. **Create system prompt** in `backend/app/personas/registry.py`
2. **Define PersonaConfig** with ID, description, and output mode
3. **Register in PERSONA_REGISTRY** dictionary
4. **Set LLM provider** in `PERSONA_PROVIDER_MAP` (in `llm_client.py`)
5. **Frontend updates automatically** from `/api/personas` endpoint

### Modify Streaming Behavior

Edit `/backend/app/routers/chat.py` to customize:
- Context retrieval strategy
- Prompt injection logic
- Response formatting

### Style Customization

All styling in `/backend/static/css/styles.css`:
- Change color scheme (CSS variables at top)
- Adjust terminal font and sizing
- Customize UI card layouts

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| **Port 8080 already in use** | `python -m uvicorn app.main:app --port 8081` |
| **API key errors** | Verify `.env` file has correct keys, restart server |
| **PDF upload fails** | Check file size (10MB limit), ensure PDF is not corrupted |
| **Streaming stops mid-response** | Check browser console for errors, verify API key quotas |
| **CORS errors** | Ensure `CORS_ORIGINS` in `.env` includes your frontend URL |
| **Database errors** | Ensure `DATABASE_URL` is set and Neon is reachable |
| **Rate limiting errors** | Ensure `REDIS_URL` is set and Upstash is reachable |

---

## 🔐 Security Notes

- ✅ **Semantic vector retrieval** — document answers are grounded via Qdrant embeddings, not hallucinated
- ✅ **bcrypt password hashing** — user passwords are never stored in plaintext
- ✅ **JWT authentication** — all API endpoints require valid tokens
- ✅ **Guest access** — anonymous demo tokens with 4-hour expiry (no password required)
- ✅ **Rate limiting** — Redis-backed per-IP limits, fails closed when Redis is down
- ✅ **CORS configured** — restricts cross-origin requests
- ⚠️ **API keys** — keep `.env` private, never commit to version control

---

## 📝 Sample Use Cases

### Academic
- 📖 Study for exams with interactive Socratic tutoring
- 📚 Analyze research papers with ground-truth extraction
- 🔬 Synthesize literature across multiple sources

### Professional
- 💼 Get resume feedback before applying
- 🔐 Security-audit your codebase
- 👨‍💻 Pair-program complex features with AI colleague

### Development
- 🐛 Catch bugs before code review
- 📊 Analyze performance bottlenecks
- 🏗️ Get architecture recommendations

---

## 📜 License

This project is open source and available under the MIT License.

---

## 🤝 Contributing

Found a bug? Have an idea for a new persona? 
1. Fork the repo
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 💬 Questions?

- 📧 Open an issue on GitHub
- 💡 Check existing discussions
- 🚀 See deployment guides in `/docs` (coming soon)

---

## ⭐ Give It a Star!

If you found this project useful, please star it on GitHub. It helps other developers discover this tool.

**[⭐ Star on GitHub](https://github.com/Ysaibhanu99/Klyvix)**

---

## 🎯 Roadmap

- [ ] Web UI customization panel
- [ ] Export conversations as PDF reports
- [ ] Multi-language support
- [ ] Chrome extension for quick access
- [ ] Team collaboration features
- [ ] Custom persona builder

---

**Built with ❤️ by Ysaibhanu99**

*Last updated: August 2026*
