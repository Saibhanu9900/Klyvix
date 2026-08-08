import asyncio
import logging
from typing import AsyncGenerator, List, Dict, Any, Optional
# pyrefly: ignore [missing-import]
from google import genai
# pyrefly: ignore [missing-import]
from google.genai import types
from groq import AsyncGroq
from httpx import AsyncClient
from app.core.config import settings
from app.personas.registry import PERSONA_TEMPERATURES

logger = logging.getLogger(__name__)

# Initialize clients if keys exist
gemini_client = genai.Client(api_key=settings.GEMINI_API_KEY) if settings.GEMINI_API_KEY else None
groq_client = AsyncGroq(api_key=settings.GROQ_API_KEY) if settings.GROQ_API_KEY else None
mistral_http_client = AsyncClient(
    base_url="https://api.mistral.ai/v1",
    headers={"Authorization": f"Bearer {settings.MISTRAL_API_KEY}"},
    timeout=30.0
) if settings.MISTRAL_API_KEY else None

# Per-persona primary provider mapping (from API_per_personas.md)
PERSONA_PROVIDER_MAP: Dict[str, str] = {
    "study_mentor": "gemini",
    "code_reviewer": "mistral",      # Codestral — specialized for code
    "code_colleague": "mistral",     # Codestral — code generation & pair programming
    "document_analyzer": "gemini",
    "resume_reviewer": "gemini",
    "research_assistant": "gemini",
}

# ─── Gemini Streaming ────────────────────────────────────────────────────────

def prepare_gemini_messages(system_prompt: str, history: List[Dict[str, str]], user_message: str, temperature: float = 0.7, use_search: bool = False):
    """Formats system prompt, conversation history, and current query into Gemini contents."""
    contents = []
    
    # Add history
    for msg in history:
        role = "user" if msg.get("role") == "user" else "model"
        contents.append(types.Content(
            role=role,
            parts=[types.Part.from_text(text=msg.get("content", ""))]
        ))
        
    # Add current user message
    contents.append(types.Content(
        role="user",
        parts=[types.Part.from_text(text=user_message)]
    ))
    
    config = types.GenerateContentConfig(
        system_instruction=system_prompt,
        temperature=temperature,
    )
    if use_search:
        config.tools = [types.Tool(google_search=types.GoogleSearch())]
    return contents, config

async def stream_gemini(system_prompt: str, history: List[Dict[str, str]], user_message: str, temperature: float = 0.7, use_search: bool = False) -> AsyncGenerator[str, None]:
    """Streams responses from Gemini 2.5 Flash asynchronously."""
    if not gemini_client:
        raise ValueError("GEMINI_API_KEY is missing.")
        
    contents, config = prepare_gemini_messages(system_prompt, history, user_message, temperature, use_search)
    
    # Run sync streaming iterator in a thread executor to avoid blocking the asyncio event loop
    loop = asyncio.get_event_loop()
    
    def get_stream():
        return gemini_client.models.generate_content_stream(
            model=settings.GEMINI_MODEL,
            contents=contents,
            config=config
        )
        
    response_stream = await loop.run_in_executor(None, get_stream)
    
    for chunk in response_stream:
        if chunk.text:
            yield chunk.text

# ─── Mistral / Codestral Streaming ───────────────────────────────────────────

async def stream_mistral(system_prompt: str, history: List[Dict[str, str]], user_message: str, temperature: float = 0.7) -> AsyncGenerator[str, None]:
    """Streams responses from Mistral Codestral for code-specialized tasks."""
    if not mistral_http_client:
        raise ValueError("MISTRAL_API_KEY is missing.")
    
    messages = [{"role": "system", "content": system_prompt}]
    for msg in history:
        role = "user" if msg.get("role") == "user" else "assistant"
        messages.append({"role": role, "content": msg.get("content", "")})
    messages.append({"role": "user", "content": user_message})
    
    payload = {
        "model": settings.MISTRAL_MODEL,
        "messages": messages,
        "temperature": temperature,
        "stream": True
    }
    
    async with mistral_http_client.stream("POST", "/chat/completions", json=payload) as response:
        if response.status_code != 200:
            error_body = await response.aread()
            raise Exception(f"Mistral API error {response.status_code}: {error_body.decode()}")
        
        async for line in response.aiter_lines():
            if not line.startswith("data: "):
                continue
            data_str = line[6:].strip()
            if data_str == "[DONE]":
                break
            try:
                import json
                chunk = json.loads(data_str)
                delta = chunk.get("choices", [{}])[0].get("delta", {}).get("content")
                if delta:
                    yield delta
            except Exception:
                continue

# ─── Groq Streaming (Global Fallback) ────────────────────────────────────────

async def stream_groq(system_prompt: str, history: List[Dict[str, str]], user_message: str, temperature: float = 0.7) -> AsyncGenerator[str, None]:
    """Streams responses from Groq Llama 3.3 70B as fallback."""
    if not groq_client:
        raise ValueError("GROQ_API_KEY is missing.")
        
    messages = [{"role": "system", "content": system_prompt}]
    for msg in history:
        role = "user" if msg.get("role") == "user" else "assistant"
        messages.append({"role": role, "content": msg.get("content", "")})
    messages.append({"role": "user", "content": user_message})
    
    response = await groq_client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=messages,
        temperature=temperature,
        stream=True
    )
    
    async for chunk in response:
        delta = chunk.choices[0].delta.content if chunk.choices else None
        if delta:
            yield delta

# ─── Unified LLM Router with Per-Persona Provider + Fallback ─────────────────

import datetime
import hashlib
import json
from app.core.cache import cache

def generate_cache_key(system_prompt: str, history: List[Dict[str, str]], user_message: str, persona_id: str) -> str:
    """Generates a unique cache key based on the prompt inputs."""
    data = json.dumps({
        "system": system_prompt,
        "history": history,
        "user": user_message,
        "persona": persona_id
    }, sort_keys=True)
    return f"llm_cache:{hashlib.sha256(data.encode()).hexdigest()}"

async def call_llm_stream(
    system_prompt: str,
    history: List[Dict[str, str]],
    user_message: str,
    persona_id: str = ""
) -> AsyncGenerator[str, None]:
    """Routes to the correct primary provider per persona, with Groq fallback and Redis caching."""
    
    # Check cache first
    cache_key = generate_cache_key(system_prompt, history, user_message, persona_id)
    cached_response = await cache.get(cache_key)
    
    if cached_response:
        logger.info(f"[{persona_id}] Cache hit! Returning cached response.")
        # Yield in chunks to simulate streaming
        chunk_size = 50
        for i in range(0, len(cached_response), chunk_size):
            yield cached_response[i:i+chunk_size]
            await asyncio.sleep(0.01)
        return
    
    # Inject current date so the model knows the present year
    current_date = datetime.datetime.now().strftime("%B %d, %Y")
    system_prompt += f"\n\n[SYSTEM NOTE: The current date is {current_date}. Always treat {current_date} as the present. Use your search tools for any current events or recent information.]"
    
    primary = PERSONA_PROVIDER_MAP.get(persona_id, "gemini")
    temperature = PERSONA_TEMPERATURES.get(persona_id, 0.7)
    
    partial_response = ""
    tokens_yielded = 0
    
    # --- Attempt primary provider ---
    try:
        # Simple retry logic for transient errors
        for attempt in range(2):
            try:
                if primary == "mistral" and settings.MISTRAL_API_KEY:
                    logger.info(f"[{persona_id}] Calling primary provider: Mistral (Codestral)")
                    async for token in stream_mistral(system_prompt, history, user_message, temperature):
                        partial_response += token
                        tokens_yielded += 1
                        yield token
                    await cache.set(cache_key, partial_response, expire_seconds=86400)
                    return
                elif primary == "gemini" and settings.GEMINI_API_KEY:
                    logger.info(f"[{persona_id}] Calling primary provider: Gemini")
                    use_search = persona_id == "research_assistant"
                    async for token in stream_gemini(system_prompt, history, user_message, temperature, use_search=use_search):
                        partial_response += token
                        tokens_yielded += 1
                        yield token
                    await cache.set(cache_key, partial_response, expire_seconds=86400)
                    return
                else:
                    raise ValueError(f"Primary provider '{primary}' key is not configured.")
            except Exception as e:
                # If we've yielded tokens, we can't retry the primary transparently without resetting the stream
                if tokens_yielded > 0:
                    raise e # Break out to fallback to continue the stream
                if attempt == 0:
                    logger.warning(f"[{persona_id}] Primary provider ({primary}) failed on attempt {attempt+1}: {e}. Retrying in 1s...")
                    await asyncio.sleep(1)
                else:
                    raise e
    except Exception as e:
        logger.warning(f"[{persona_id}] Primary provider ({primary}) failed: {e}. Attempting Groq fallback...")
    
    # --- Fallback to Groq ---
    if settings.GROQ_API_KEY:
        logger.info(f"[{persona_id}] Calling fallback provider: Groq (tokens yielded: {tokens_yielded})")
        
        fallback_history = history.copy()
        fallback_user_message = user_message
        
        # If we failed mid-stream, we instruct the fallback to continue
        if tokens_yielded > 0:
            fallback_user_message = (
                f"{user_message}\n\n"
                f"[SYSTEM NOTE: The previous response was interrupted. "
                f"Continue the following response exactly in the same tone and format, without repeating the partial response:]\n"
                f"{partial_response}"
            )
            
        try:
            async for token in stream_groq(system_prompt, fallback_history, fallback_user_message, temperature):
                partial_response += token
                yield token
            await cache.set(cache_key, partial_response, expire_seconds=86400)
            return
        except Exception as e:
            logger.error(f"[{persona_id}] Groq fallback also failed: {e}")
            yield f"\n\n[Error: All LLM providers unavailable — {str(e)}]"
    else:
        yield f"\n\n[Error: Primary provider failed and GROQ_API_KEY is not configured for fallback.]"

async def get_embeddings(texts: List[str]) -> List[List[float]]:
    """Generates text embeddings using Gemini embedding model."""
    if not gemini_client:
        raise ValueError("GEMINI_API_KEY is missing.")
    
    loop = asyncio.get_event_loop()
    def embed():
        response = gemini_client.models.embed_content(
            model='gemini-embedding-2',
            contents=texts
        )
        return [e.values for e in response.embeddings]
        
    return await loop.run_in_executor(None, embed)
