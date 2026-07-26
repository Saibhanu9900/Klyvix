import json
from typing import AsyncGenerator
from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import StreamingResponse

from app.core.rate_limit import rate_limiter
from app.models.schemas import ChatRequest
from app.personas.registry import get_persona
from app.core.retrieval import get_top_k_chunks, document_store
from app.core.llm_client import call_llm_stream

router = APIRouter(prefix="/api", tags=["chat"])

async def sse_event_generator(system_prompt: str, history: list, user_message: str, persona_id: str = "") -> AsyncGenerator[str, None]:
    """Wraps LLM token stream into SSE data events."""
    try:
        async for token in call_llm_stream(system_prompt, history, user_message, persona_id=persona_id):
            # Encode token into JSON payload for safe line breaks/quotes
            data = json.dumps({"token": token})
            yield f"data: {data}\n\n"
        yield "data: [DONE]\n\n"
    except Exception as e:
        error_data = json.dumps({"error": str(e)})
        yield f"data: {error_data}\n\n"

@router.post("/chat/{persona_id}", dependencies=[Depends(rate_limiter)])
async def chat_persona(persona_id: str, request: ChatRequest, req: Request):
    """Streaming chat endpoint for all 6 personas."""
    persona = get_persona(persona_id)
    if not persona:
        raise HTTPException(status_code=404, detail=f"Persona '{persona_id}' not found.")

    system_prompt = persona.system_prompt
    user_message = request.message
    
    # Sliding history window (keep last 10 messages)
    history = [msg.model_dump() for msg in request.history[-10:]]

    # Context Retrieval (Global across multiple files)
    retrieved_context = ""
    if getattr(request, "file_ids", None):
        retrieved_context = await get_top_k_chunks(request.file_ids, user_message)

    # Persona-specific prompt injection
    if persona_id == "document_analyzer":
        if not getattr(request, "file_ids", None):
            raise HTTPException(status_code=400, detail="Document Analyzer requires at least one uploaded file.")
        system_prompt = system_prompt.format(
            retrieved_chunks=retrieved_context,
            user_question=user_message
        )
    elif persona_id == "research_assistant":
        # Research Assistant uses Google Search grounding — no prompt placeholders needed
        # If user uploaded docs, append context to the message
        if retrieved_context and retrieved_context != "No document context available.":
            user_message = f"{user_message}\n\n[Context from attached document(s):]\n{retrieved_context}"
    else:
        # For all other personas (Study Mentor, Code/Resume Reviewer), append context dynamically
        if retrieved_context and retrieved_context != "No document context available.":
            user_message = f"{user_message}\n\n[Context from attached document(s):]\n{retrieved_context}"

    return StreamingResponse(
        sse_event_generator(system_prompt, history, user_message, persona_id=persona_id),
        media_type="text/event-stream"
    )
