# AI Command Center

> A unified platform housing 6 specialized AI personas, each engineered for distinct academic and professional tasks.

[![Python](https://img.shields.io/badge/Python-43.7%25-blue)](https://www.python.org/)
[![JavaScript](https://img.shields.io/badge/JavaScript-30.5%25-yellow)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## Overview

**AI Command Center** is a production-ready platform that provides six distinct AI-powered personas optimized for different use cases. Instead of a one-size-fits-all chatbot, each persona is engineered with specialized prompting and capabilities to deliver targeted, high-quality assistance.

### Key Features

- **6 Specialized Personas**: Study Mentor, Code Reviewer, Code Colleague, Document Analyzer, Resume Reviewer, Research Assistant
- **Dual LLM Strategy**: Google Gemini as primary provider with Groq automatic fallback
- **Real-time Streaming**: Progressive token streaming for responsive user experience
- **Document Intelligence**: PDF upload and keyword-based retrieval for grounded answers
- **Structured Output**: JSON-based responses for Code/Resume reviews with categorized feedback
- **Responsive Web UI**: Modern terminal-inspired interface with dark/light themes
- **Docker Ready**: Single containerized deployment for AWS or any cloud platform
- **Cost Optimized**: Built to stay within free-tier limits of all services

---

## Project Structure

```
AI_COMMAND_CENTER/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI application entry point
│   │   ├── core/
│   │   │   ├── config.py            # Environment configuration & settings
│   │   │   ├── llm_client.py         # Gemini/Groq streaming & fallback logic
│   │   │   ├── retrieval.py          # PDF chunking & keyword retrieval
│   │   │   └── rate_limit.py         # Request rate limiting
│   │   ├── models/
│   │   │   └── schemas.py            # Pydantic request/response models
│   │   ├── personas/
│   │   │   └── registry.py           # Persona configuration registry
│   │   └── routers/
│   │       ├── chat.py               # POST /api/chat/{persona_id} streaming endpoint
│   │       └── upload.py             # POST /api/upload PDF handling
│   ├── static/
│   │   ├── index.html                # Frontend shell (React/HTML)
│   │   ├── css/
│   │   │   └── styles.css            # Styling
│   │   └── js/
│   │       ├── api.js                # API client wrapper
│   │       ├── app.js                # Main app logic
│   │       └── components/           # UI components
│   ├── requirements.txt              # Python dependencies
│   ├── .env.example                  # Environment template
│   ├── generate_research_pdf.py      # PDF generation utilities
│   └── generate_sample_pdf.py
├── files/                            # Documentation
│   ├── architecture.md               # System architecture & design
│   ├── prd.md                        # Product requirements document
│   ├── prompt-design.md              # Prompt engineering documentation
│   ├── phases.md                     # Development timeline
│   ├── API_per_personas.md           # API specifications per persona
│   ├── Elite_Terminal_Frontend_Spec.md
│   ├── enhanced_system_prompts.md
│   ├── code_colleague_enhanced_prompt.md
│   ├── memory.md                     # Session memory handling
│   └── rules.md                      # Design rules & constraints
├── Dockerfile                        # Container configuration
├── .gitignore
└── README.md
```

---

## Stack

| Component | Technology |
|-----------|------------|
| **Backend** | FastAPI 0.110+, Python 3.12 |
| **Frontend** | HTML/CSS/JavaScript with KaTeX & Marked for rendering |
| **LLM Integration** | Google Gemini API (primary), Groq API (fallback) |
| **PDF Processing** | pypdf 4.1+ |
| **Streaming** | Server-Sent Events (SSE) |
| **Containerization** | Docker |
| **Deployment** | AWS App Runner (recommended) |

### Key Dependencies

- **fastapi** — Web framework
- **uvicorn** — ASGI server
- **pydantic** — Data validation
- **google-genai** — Gemini API client
- **groq** — Groq API client
- **pypdf** — PDF text extraction & chunking
- **python-dotenv** — Environment variable management

---

## The 6 Personas

### 1. **Study Mentor**
An adaptive tutor that checks understanding progressively, asks follow-up questions, and re-explains concepts if needed.

### 2. **Code Reviewer**
Structured code feedback across three dimensions: Bugs/Correctness, Security, and Style.

### 3. **Code Colleague**
A peer programmer offering practical code suggestions and collaborative debugging advice.

### 4. **Document Analyzer**
Grounded question-answering directly from uploaded PDFs using keyword-based retrieval. Explicitly states when answers aren't in the document.

### 5. **Resume Reviewer**
Structured resume feedback with categorized strengths, gaps, and actionable suggestions including before/after rewrites.

### 6. **Research Assistant**
Synthesizes multiple PDF sources or text blocks into coherent answers, flagging agreements and conflicts between sources.

---

## Getting Started

### Prerequisites

- Python 3.12+
- Docker (optional, for containerized deployment)
- API Keys:
  - Google Gemini API key ([get one](https://ai.google.dev/))
  - Groq API key ([get one](https://console.groq.com/))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Ysaibhanu99/AI_COMMAND_CENTER.git
   cd AI_COMMAND_CENTER
   ```

2. **Set up environment variables**
   ```bash
   cp backend/.env.example backend/.env
   ```

   Edit `backend/.env` with your API keys:
   ```dotenv
   GEMINI_API_KEY=your_gemini_api_key_here
   GROQ_API_KEY=your_groq_api_key_here
   MISTRAL_API_KEY=your_mistral_api_key_here
   PORT=8080
   HOST=0.0.0.0
   CORS_ORIGINS=["*"]
   ```

3. **Install dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

### Running Locally

#### Development Mode
```bash
cd backend
python -m app.main
```

The API will be available at `http://localhost:8080`
- Interactive API docs: `http://localhost:8080/docs`
- ReDoc documentation: `http://localhost:8080/redoc`

#### Using Docker
```bash
docker build -t ai-command-center .
docker run -p 8080:8080 \
  -e GEMINI_API_KEY=your_key \
  -e GROQ_API_KEY=your_key \
  ai-command-center
```

---

## API Endpoints

### Chat Endpoint
**POST** `/api/chat/{persona_id}`

Stream responses from a specific persona.

**Parameters:**
- `persona_id` (path): One of `study_mentor`, `code_reviewer`, `code_colleague`, `document_analyzer`, `resume_reviewer`, `research_assistant`

**Request Body:**
```json
{
  "message": "Your question or code here",
  "history": [
    {"role": "user", "content": "previous message"},
    {"role": "assistant", "content": "previous response"}
  ],
  "file_ids": ["optional_file_id_from_upload"]
}
```

**Response:** Server-Sent Events stream of tokens

**Example:**
```bash
curl -X POST "http://localhost:8080/api/chat/study_mentor" \
  -H "Content-Type: application/json" \
  -d '{"message": "Explain quantum entanglement", "history": []}'
```

### Upload Endpoint
**POST** `/api/upload`

Upload one or more PDF documents for Document Analyzer or Research Assistant.

**Request:** Multipart form with PDF files

**Response:**
```json
[
  {
    "file_id": "doc_1",
    "filename": "research_paper.pdf",
    "total_chunks": 12,
    "total_words": 3456
  }
]
```

**Example:**
```bash
curl -X POST "http://localhost:8080/api/upload" \
  -F "files=@research_paper.pdf" \
  -F "files=@test_document.pdf"
```

### Health Check
**GET** `/api/health`

```json
{"status": "ok", "service": "AI Command Center Backend"}
```

### List Personas
**GET** `/api/personas`

Returns metadata for all available personas with their capabilities.

---

## How It Works

### Request Flow

1. User submits a message from a persona workspace
2. Frontend POSTs to `/api/chat/{persona_id}` with optional file context
3. Backend loads persona configuration and system prompt
4. If documents are attached, retrieves top-k relevant chunks via keyword matching
5. Constructs message payload (system prompt + history + user input + context)
6. Streams response from Gemini API (falls back to Groq on failure)
7. Frontend displays tokens in real-time as they arrive

### Document Retrieval Pipeline

For personas requiring document intelligence (Document Analyzer, Research Assistant):

1. **Upload Phase**: PDF text extracted and split into ~300-500 word chunks with 50-word overlap
2. **Query Phase**: User message tokenized and compared against chunks
3. **Scoring**: Simple term-frequency scoring identifies top-k matching chunks
4. **Injection**: Context injected into system prompt for grounded responses
5. **Verification**: Persona prompted to explicitly state if answer isn't in documents

---

## Configuration

All configuration is managed through environment variables (never hardcoded). See `backend/app/core/config.py` for available options:

| Variable | Default | Purpose |
|----------|---------|---------|
| `GEMINI_API_KEY` | — | Google Gemini API key (required) |
| `GROQ_API_KEY` | — | Groq API key (required) |
| `MISTRAL_API_KEY` | — | Mistral API key (optional) |
| `PORT` | 8080 | Server port |
| `HOST` | 0.0.0.0 | Server host |
| `CORS_ORIGINS` | ["*"] | CORS allowed origins |
| `GEMINI_MODEL` | gemini-2.5-flash | Gemini model to use |
| `GROQ_MODEL` | llama-3.3-70b-versatile | Groq fallback model |

---

## Development

### Project Documentation

Detailed documentation is available in the `files/` directory:

- **[architecture.md](files/architecture.md)** — System design, data flow, deployment strategy
- **[prd.md](files/prd.md)** — Product requirements, personas, success metrics
- **[prompt-design.md](files/prompt-design.md)** — Prompt engineering methodology and examples
- **[phases.md](files/phases.md)** — Development timeline and milestones
- **[API_per_personas.md](files/API_per_personas.md)** — Detailed API specs per persona
- **[enhanced_system_prompts.md](files/enhanced_system_prompts.md)** — Complete prompt engineering documentation
- **[rules.md](files/rules.md)** — Design constraints and principles

### Running Tests

```bash
# Run the sample PDF generators to validate PDF processing
python backend/generate_sample_pdf.py
python backend/generate_research_pdf.py
```

### Code Style

The project follows PEP 8 conventions. Use type hints throughout for better IDE support and maintainability.

---

## Deployment

### AWS App Runner (Recommended)

1. Push code to GitHub
2. Create App Runner service from GitHub repository
3. Configure environment variables in App Runner console
4. Set up AWS Budget Alerts (recommended: $1 and $5 thresholds)
5. App Runner provides automatic HTTPS URL

### Docker + Any Cloud

```bash
# Build
docker build -t ai-command-center:latest .

# Tag for registry
docker tag ai-command-center:latest your-registry/ai-command-center:latest

# Push
docker push your-registry/ai-command-center:latest

# Deploy with your cloud provider
```

---

## Security

- ✅ All API keys loaded from environment variables
- ✅ `.env` added to `.gitignore` by default
- ✅ CORS configured to allow only frontend origins
- ✅ Input validation on file uploads (PDF only, 10MB limit)
- ✅ No user identifying data stored beyond active session
- ✅ HTTPS enforced in production

---

## Cost Management

All services are designed to operate within free tiers:

- **Google Gemini**: Free tier available for development
- **Groq**: Free API tier with generous limits
- **AWS App Runner**: Free tier (750 hours/month @ 0.5 GB, 0.25 vCPU)
- **No database**: In-memory storage for development (session-only)

**Recommendation**: Set AWS Budget Alerts immediately after account setup.

---

## Troubleshooting

### API Keys Not Working

```bash
# Verify .env file is loaded
ls -la backend/.env

# Check the file has correct format
cat backend/.env
```

### Port Already in Use

```bash
# Change PORT in .env
PORT=8081

# Or kill the process using port 8080
lsof -ti:8080 | xargs kill -9
```

### Docker Build Fails

```bash
# Clear build cache
docker build --no-cache -t ai-command-center .

# Check Docker daemon
docker ps
```

### LLM Calls Timing Out

- Verify API keys are valid
- Check rate limits on LLM provider accounts
- Increase timeout in production settings

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

---

## Roadmap

- [ ] Vector embeddings & semantic search for Document Analyzer
- [ ] Persistent session storage with database
- [ ] User authentication & multi-user support
- [ ] Custom persona builder UI
- [ ] Advanced analytics dashboard
- [ ] Batch processing API
- [ ] Export to multiple formats (PDF, Markdown, JSON)

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Author

**Ysaibhanu99** — [GitHub Profile](https://github.com/Ysaibhanu99)

---

## Support

For questions, issues, or feedback:

- 📝 [Open an Issue](https://github.com/Ysaibhanu99/AI_COMMAND_CENTER/issues)
- 💬 [Discussions](https://github.com/Ysaibhanu99/AI_COMMAND_CENTER/discussions)
- 📧 Check the repository for contact information

---

**Built with ❤️ for educators, students, and developers.**
