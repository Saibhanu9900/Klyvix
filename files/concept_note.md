# HexaMind — Concept Note

## Project Title
**HexaMind: AI Command Center** — A Unified Multi-Persona AI Platform for Academic & Professional Workflows

## Team
- **Team Size**: 6 members
- **Course**: Gen AI & Cloud Computing — Vibe Coding Final Project
- **Timeline**: 5-Day Sprint

---

## 1. Problem Statement

Students and early-career professionals regularly interact with general-purpose AI chatbots (ChatGPT, Gemini, etc.) for tasks ranging from studying to code review to document analysis. However, a single generic chatbot fails when asked to handle fundamentally different workflows:

- **Learning**: Chatbots dump full explanations instead of guiding the student through understanding step-by-step (Socratic method).
- **Code Review**: Generic chatbots produce unstructured feedback. Real code review requires categorized, actionable output (bugs, security, performance, style) — not a paragraph.
- **Document Q&A**: Chatbots hallucinate answers. When a user uploads a PDF and asks a question, the answer must come *strictly* from the document, not from the model's training data.
- **Resume Feedback**: Users need structured before/after rewrites, not vague advice like "make your bullet points more impactful."
- **Multi-Source Research**: Synthesizing findings from multiple documents requires explicit cross-referencing, agreement/conflict flagging — not source-by-source summaries.

**HexaMind** solves this by housing **six specialized AI personas** behind one platform, each with meaningfully different prompt engineering, behavior rules, and output structures.

---

## 2. Proposed Solution

A single-container, full-stack web application built with:

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| **Backend** | FastAPI (Python) | Native async support, streaming via `StreamingResponse`, fast prototyping |
| **Frontend** | Vanilla HTML/CSS/JS | Zero build step, maximum control, terminal-inspired UI aesthetic |
| **Primary LLM** | Google Gemini API | High-quality reasoning, generous free tier |
| **Fallback LLM** | Groq API (Mixtral/Llama) | Ultra-fast inference, automatic fallback when Gemini rate-limits or fails |
| **Deployment** | AWS (App Runner / Elastic Beanstalk) | Single Docker container, auto-HTTPS, free-tier eligible |

### Architecture Principle
Personas are **data** (configuration objects), not separate services. One shared routing, streaming, and LLM-calling codebase serves all six personas — only the system prompt, output mode, and behavior rules differ per persona.

---

## 3. The Six AI Personas

### 3.1 Study Mentor
- **Mode**: Conversational (freeform dialogue)
- **Key Behavior**: Socratic teaching — breaks concepts into pieces, asks check-in questions, re-explains on misunderstanding, ends with recaps
- **Differentiator**: Never dumps a full explanation; always verifies understanding before advancing

### 3.2 Code Reviewer
- **Mode**: Structured JSON output
- **Key Behavior**: Audits code across four categories — Bugs/Correctness, Security, Performance, Style
- **Differentiator**: Each issue includes location, severity, explanation, and a concrete fix suggestion

### 3.3 Code Colleague
- **Mode**: Conversational (freeform dialogue)
- **Key Behavior**: Pair-programming partner for code generation, refactoring, debugging, and architecture
- **Differentiator**: Collaborative tone, explains design decisions, provides working code with inline comments

### 3.4 Document Analyzer
- **Mode**: Conversational with context injection
- **Key Behavior**: Answers questions strictly from uploaded PDF content; refuses to answer if the answer isn't in the document
- **Differentiator**: Custom keyword-based chunk retrieval pipeline (no embeddings/RAG) — deliberately simple and transparent

### 3.5 Resume Reviewer
- **Mode**: Structured JSON output
- **Key Behavior**: Evaluates resumes across Strengths, Gaps, and Concrete Suggestions
- **Differentiator**: Every suggestion includes a before/after rewrite example — not generic advice

### 3.6 Research Assistant
- **Mode**: Conversational with multi-source synthesis
- **Key Behavior**: Combines multiple PDFs and pasted text into thematic synthesis; flags agreements and conflicts between sources
- **Differentiator**: Synthesizes by theme, not source-by-source summarization

---

## 4. Key Technical Features

### 4.1 Intelligent LLM Fallback
```
User Request → Gemini API (primary)
                  ↓ (on failure / rate-limit / 5xx)
              Groq API (automatic fallback)
```
The user never sees a retry prompt. If Gemini fails, Groq takes over transparently within the same streaming response.

### 4.2 Real-Time Streaming
All responses stream token-by-token via Server-Sent Events (SSE). The first token appears within ~2-3 seconds. The terminal-style UI renders responses progressively — no waiting for the full response before displaying.

### 4.3 PDF Processing Pipeline
- Text extraction via `pypdf`
- Chunking: ~300-500 words per chunk with ~50-word overlap
- Retrieval: keyword/token-overlap scoring (term-frequency based)
- Top-k chunks injected into the prompt as labeled excerpts

### 4.4 Terminal-Inspired UI
A dark, monospaced, zero-border-radius interface inspired by real terminal environments. User inputs render as `$ commands`, outputs render as stdout, with `[processing...]` indicators between input and response.

---

## 5. Prompt Engineering Approach

Each persona's system prompt is purpose-built with:
1. **Role definition** — Who the persona is and what it's optimized for
2. **Behavioral constraints** — What it must do and must NOT do
3. **Output structure specification** — Freeform text vs. strict JSON schema
4. **Tone calibration** — Socratic questioning (Study Mentor) vs. professional audit (Code Reviewer)

The prompts are documented with rationale and sample input/output in the companion `prompt-design.md` document.

---

## 6. Deployment Strategy

- **Containerization**: Single Dockerfile bundles backend + frontend static assets
- **Cloud**: AWS App Runner (recommended) — automatic HTTPS, single container, minimal config
- **Security**: All API keys via environment variables; CORS locked to deployed origin; no secrets in git history
- **Budget**: AWS Budget Alerts configured at $1 and $5 thresholds before heavy usage begins

---

## 7. Expected Outcomes

1. A live, publicly accessible application at an AWS HTTPS URL
2. Six functionally distinct AI personas demonstrating real prompt engineering differentiation
3. Seamless LLM failover ensuring high availability
4. A terminal-aesthetic UI that is both functional and visually distinctive
5. Complete documentation (this Concept Note + Project Report + prompt-design docs)

---

## 8. Innovation & Differentiation

| Aspect | Generic Chatbot | HexaMind |
|--------|----------------|----------|
| Persona count | 1 (generic) | 6 (specialized) |
| Output structure | Unformatted text | JSON schemas + formatted markdown |
| Document grounding | Hallucination risk | Strict chunk-based retrieval |
| LLM reliability | Single provider | Auto-failover (Gemini → Groq) |
| UI paradigm | Standard chat bubbles | Terminal-inspired command interface |
| Teaching style | Dumps full answers | Socratic step-by-step guidance |

---

## 9. References

- `architecture.md` — System architecture and folder structure
- `prompt-design.md` — All persona system prompts with rationale and sample I/O
- `phases.md` — 5-day development plan with daily definitions of done
- `prd.md` — Full product requirements document
