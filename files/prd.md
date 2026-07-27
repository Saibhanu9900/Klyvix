# PRD — HexaMind

**Project**: Vibe Coding Final Project — Gen AI & Cloud Computing
**Team size**: 6 · **Timeline**: 5 days

---

## 1. Overview

HexaMind is a single platform housing five distinct AI-powered personas, each engineered for a specific academic/professional task. Instead of one generic chatbot reused with different names, each persona has its own prompt design, behavior rules, and output structure — the engineering differs meaningfully persona-to-persona.

## 2. Goals

- Ship five working, meaningfully-different AI personas behind one platform
- Demonstrate real prompt engineering differentiation (not just cosmetic differences)
- Deploy a live, publicly accessible, containerized app on AWS within free-tier limits
- Produce documentation strong enough to satisfy the course's process/reflection requirements

## 3. Non-Goals / Out of Scope

- No vector embeddings / RAG for Document Analyzer — keyword-based retrieval + chunking only, by deliberate scope decision
- No user authentication / accounts (out of scope unless time permits after core features are done)
- No persistent database of past sessions (in-memory / session-only state unless time allows)
- No multi-language support beyond whatever the underlying LLM handles natively

## 4. Target Users & Use Cases

Students and early-career professionals who need fast, structured AI help across academic and job-related tasks: learning a new topic, reviewing code for an assignment or project, extracting answers from long PDFs, polishing a resume, and synthesizing findings across multiple reference documents.

## 5. Personas — Functional Requirements

### 5.1 Study Mentor
- **User story**: As a student, I want a tutor that checks my understanding instead of dumping a full explanation, so I actually retain the concept.
- **Acceptance criteria**: Response breaks concepts into pieces; asks a follow-up/check-in question before advancing; re-explains if the user's answer shows a misunderstanding; ends topics with a short recap.

### 5.2 Code Reviewer
- **User story**: As a developer, I want my code reviewed across bugs, security, and style separately, so I can prioritize fixes.
- **Acceptance criteria**: Output always has three distinct sections (Bugs/Correctness, Security, Style); each issue includes location, why it matters, and a suggested fix; empty categories are explicitly stated as clean, not omitted.

### 5.3 Document Analyzer
- **User story**: As a student, I want to upload a PDF and ask questions answered strictly from that document, so I don't get hallucinated answers.
- **Acceptance criteria**: Answers are grounded only in retrieved chunks; if the answer isn't in the document, the assistant says so explicitly rather than guessing; retrieval uses chunking + keyword matching (no embeddings/RAG).

### 5.4 Resume Reviewer
- **User story**: As a job-seeker, I want structured feedback on my resume, so I know exactly what to fix.
- **Acceptance criteria**: Output has three sections (Strengths, Gaps, Concrete Suggestions); at least one suggestion includes a before/after rewrite example, not just generic advice.

### 5.5 Research Assistant
- **User story**: As a student, I want to combine multiple sources into one coherent answer, so I don't have to manually cross-reference them myself.
- **Acceptance criteria**: Output synthesizes by theme/sub-question rather than summarizing source-by-source; agreements and conflicts between sources are explicitly flagged; accepts both PDF uploads and pasted text as sources.

## 6. System-Wide Functional Requirements

- [ ] Responsive frontend, usable on both desktop and mobile
- [ ] Backend (FastAPI) handles all routing; no API keys ever reach the frontend
- [ ] LLM integration streams responses progressively (no full-delay dump)
- [ ] Gemini API as primary LLM provider; Groq API as automatic fallback on failure/rate-limit
- [ ] Full app containerized with a working Dockerfile
- [ ] Deployed live on AWS with a public HTTPS URL
- [ ] Env vars used for all secrets; nothing sensitive committed to git
- [ ] AWS budget alerts configured before/at deployment

## 7. Non-Functional Requirements

- **Performance**: first streamed token should appear within ~2-3 seconds under normal conditions
- **Reliability**: if Gemini fails or rate-limits, Groq fallback should trigger without the user needing to retry manually
- **Cost**: must stay within AWS and LLM provider free tiers for the duration of development and grading
- **Usability**: each persona's workspace should be discoverable from a single dashboard without instructions

## 8. Success Metrics (mapped to grading)

| Grading Criteria | Weight | What "done well" looks like here |
|---|---|---|
| Technical Implementation & Vibe Coding Methodology | 25% | All 5 personas functionally distinct and working end-to-end |
| Prompt Engineering Quality & Documentation | 20% | Each persona's prompt design documented with rationale and sample I/O (see `prompt-design.md`) |
| Cloud Deployment & AWS Architecture | 20% | Live HTTPS URL, correct AWS service use, budget alerts set |
| Application Design & UX | 20% | Clean dashboard, responsive on mobile, streaming feels real-time |
| Report Quality, Reflection & Clarity | 15% | Report references actual challenges hit during the 5 days, not generic filler |

## 9. Assumptions & Open Decisions

- **Frontend framework**: not yet decided by the team. Recommend **React** for component reuse across 5 persona views — confirm at team meeting.
- **AWS deployment target**: not yet decided. Recommend **AWS App Runner** for simplicity with a single container — confirm at team meeting.
- **Team size (6)** exceeds the brief's stated cap of 2–3 — confirm with instructor whether this is acceptable before final submission.

## 10. Related Docs

`architecture.md` · `prompt-design.md` · `phases.md` · `rules.md` · `memory.md`
