# AI Command Center — Project Rules & Guidelines (`rules.md`)

## 1. System & Architecture Rules

### 1.1 LLM Client Execution & Fallback Rules
* **Primary Provider:** Google Gemini API (default for all 5 personas).
* **Fallback Provider:** Groq API (triggered automatically on 429 Rate Limit, 5xx Server Errors, or timeout > 8s).
* **Fallback Behavior:**
  * System prompts and output JSON schemas must be standardized across both providers.
  * If Gemini fails, retry once with exponential backoff (1s). If still failing, transparently route request to Groq without crashing the stream or session.
  * Log all fallback events for evaluation and cost tracking.

### 1.2 Output Standardization & Streaming
* **Server-Sent Events (SSE):** Streaming responses must be delivered using standard SSE format.
* **Structured Outputs:** Non-streaming responses or tool outputs must strictly validate against Pydantic schemas.
* **Error Handling:** Return structured error objects `{ "error": true, "message": "...", "provider": "gemini|groq" }` instead of raw stack traces.

---

## 2. Code Quality & Technical Standards

### 2.1 Backend (FastAPI)
* **Asynchronous Execution:** All endpoint route handlers and LLM streaming generators must use `async/await`.
* **Persona Config Pattern:** Each persona must be defined as an isolated configuration object containing:
  1. `persona_id`
  2. `system_prompt`
  3. `temperature` / hyper-parameters
  4. Output validation schema (Pydantic)
* **No Direct File Mutation:** Global state or file manipulations inside persona routes are prohibited. Use session handlers.

### 2.2 Security & Environment Rules
* **Zero Hardcoded Secrets:** Never hardcode API keys, AWS credentials, or host URLs in source files.
* **Environment Configuration:** Use `.env` files managed via `pydantic-settings`. Commit `.env.example` to git, never `.env`.
* **AWS Cost Safety:** Set spending thresholds in AWS Budget Alerts ($0 - $10 limit). Terminate unused resources daily.

---

## 3. Team & Repository Workflow Rules

### 3.1 Git Branching Strategy
* `main`: Deployment-ready code only.
* `dev`: Integration branch for daily milestones.
* `feature/<persona-or-feature-name>`: Individual work branches (e.g., `feature/doc-analyzer`, `feature/groq-fallback`).

### 3.2 Peer Review & Cross-Understanding
* **PR Rule:** Minimum 1 peer review approval required before merging into `dev`.
* **Knowledge Sharing Rule:** Every team member must read and understand all persona routes and client logic. *Requirement:* Any member should be capable of demonstrating any component during final project evaluation.

---

## 4. Persona & Prompt Guidelines

* **Prompt Isolation:** System prompts must live in `app/prompts/` directory, versioned as Python/YAML constants, not embedded inside API logic.
* **Prompt Structure:** Every system prompt must include:
  1. Persona Role & Identity
  2. Task Boundary / Constraints
  3. Context / Input Handling Rules
  4. Guardrails (e.g., "Do not hallucinate content outside provided context")
  5. Fallback Output Formatting