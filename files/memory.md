# AI Command Center — Memory & Context Architecture (`memory.md`)

## 1. Overview & Strategy

The AI Command Center utilizes a hybrid **Session-Based Ephemeral Memory** design. To keep performance fast, costs low, and latency low within our 5-day build, context is held in memory per session and bounded using sliding token windows.

---

## 2. Memory Types & Lifecycle

| Memory Type | Scope | Persistence | Target Component |
| :--- | :--- | :--- | :--- |
| **Session Chat History** | Per User / Per Persona | In-Memory (Dict / FastAPI App State) | All Personas (Multi-turn chat) |
| **Document Chunk Memory** | Ephemeral Request / Session | In-Memory Token Buffer | Document Analyzer / Research Assistant |
| **Persona State** | App Lifetime | Static Config File (`prompts/`) | Persona Manager |

---

## 3. Context Window & Sliding History Rules

To prevent context window overflow and keep API costs minimal:

1. **Sliding Window:** Keep only the last $N=10$ message turns (5 user requests, 5 assistant responses) in active history.
2. **Context Truncation:**
   * Maximum history length per payload: ~4,000 tokens.
   * If total tokens exceed threshold, older history is dropped, retaining the initial System Prompt + Last 4 messages + Current Query.
3. **Session Reset:** UI must include a "Clear Memory / Reset Session" trigger that purges active session history from the backend state.

---

## 4. Document & Research Memory Strategy

> **Constraint:** Vector Databases (RAG) are explicitly excluded for this project phase to maintain performance and simplicity.

* **Document Analyzer:**
  * Files (PDF / Text) uploaded by the user are parsed into text strings.
  * Extracted text is chunked into logical blocks (e.g., max 2,000 words).
  * Direct context injection is used: `System Prompt + Extracted Text Chunk + User Query`.
* **Research Assistant:**
  * Aggregates input snippets or text inputs into a temporary session buffer.
  * Stores source metadata (`source_id`, `snippet_text`) to enable key citation formatting in output streams.

---

## 5. Data Structure Schema (FastAPI State)

```python
from pydantic import BaseModel
from typing import List, Dict, Optional

class ChatMessage(BaseModel):
    role: str # "user" | "assistant" | "system"
    content: str
    timestamp: float

class SessionMemory(BaseModel):
    session_id: str
    persona_id: str
    messages: List[ChatMessage] = []
    document_context: Optional[str] = None

# Global In-Memory Store (Key: session_id)
session_store: Dict[str, SessionMemory] = {}