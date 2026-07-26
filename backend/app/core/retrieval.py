import re
import uuid
# pyrefly: ignore [missing-import]
import numpy as np
import json
import os
from typing import List, Dict, Any, Tuple
from io import BytesIO
from pypdf import PdfReader
from app.core.llm_client import get_embeddings

# Setup data directory
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
os.makedirs(DATA_DIR, exist_ok=True)
DOCUMENT_STORE_PATH = os.path.join(DATA_DIR, "document_store.json")

def load_document_store() -> Dict[str, Dict[str, Any]]:
    if os.path.exists(DOCUMENT_STORE_PATH):
        try:
            with open(DOCUMENT_STORE_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading document store: {e}")
    return {}

def save_document_store(store: Dict[str, Dict[str, Any]]):
    try:
        with open(DOCUMENT_STORE_PATH, "w", encoding="utf-8") as f:
            json.dump(store, f, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving document store: {e}")

# In-memory document store (key: file_id) loaded from disk
document_store: Dict[str, Dict[str, Any]] = load_document_store()

def extract_text_from_file(filename: str, file_bytes: bytes) -> str:
    """Extracts text from a file, supporting PDF and plain text."""
    if filename.lower().endswith(".pdf"):
        reader = PdfReader(BytesIO(file_bytes))
        extracted_text = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                extracted_text.append(f"--- Page {i + 1} ---\n{text}")
        return "\n\n".join(extracted_text)
    else:
        try:
            return file_bytes.decode('utf-8')
        except UnicodeDecodeError:
            raise ValueError(f"Could not decode {filename} as UTF-8 text.")

def chunk_text(text: str, chunk_size_words: int = 350, overlap_words: int = 50) -> List[str]:
    """Splits text into chunks of ~300-500 words with ~50-word overlap."""
    words = text.split()
    if not words:
        return []
    
    chunks = []
    start = 0
    step = chunk_size_words - overlap_words
    
    while start < len(words):
        end = min(start + chunk_size_words, len(words))
        chunk_words = words[start:end]
        chunks.append(" ".join(chunk_words))
        if end == len(words):
            break
        start += step
        
    return chunks

def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """Calculates cosine similarity between two vectors using numpy."""
    v1 = np.array(vec1)
    v2 = np.array(vec2)
    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return np.dot(v1, v2) / (norm1 * norm2)

async def store_uploaded_document(filename: str, file_bytes: bytes) -> Dict[str, Any]:
    """Extracts, chunks, embeds and stores document in memory."""
    text = extract_text_from_file(filename, file_bytes)
    chunks = chunk_text(text)
    
    # Generate embeddings for all chunks
    chunk_embeddings = await get_embeddings(chunks) if chunks else []
    
    file_id = str(uuid.uuid4())
    
    document_store[file_id] = {
        "file_id": file_id,
        "filename": filename,
        "raw_text": text,
        "chunks": chunks,
        "embeddings": chunk_embeddings,
        "word_count": len(text.split())
    }
    
    save_document_store(document_store)
    
    return {
        "file_id": file_id,
        "filename": filename,
        "total_chunks": len(chunks),
        "word_count": len(text.split())
    }

async def get_top_k_chunks(file_ids: List[str], query: str, k: int = 4) -> str:
    """Retrieves top-k scoring chunks using semantic similarity across multiple documents."""
    all_chunks = []
    all_embeddings = []
    chunk_sources = []
    
    for file_id in file_ids:
        doc = document_store.get(file_id)
        if doc and doc.get("chunks") and doc.get("embeddings"):
            all_chunks.extend(doc["chunks"])
            all_embeddings.extend(doc["embeddings"])
            # Track source file for each chunk
            for _ in range(len(doc["chunks"])):
                chunk_sources.append(doc["filename"])
                
    if not all_chunks:
        return "No document context available."
    
    # Generate embedding for the user query
    query_embed_list = await get_embeddings([query])
    if not query_embed_list:
        return "Failed to generate query embedding."
    query_embed = query_embed_list[0]
    
    scored_chunks = []
    for idx, (chunk, embed, source) in enumerate(zip(all_chunks, all_embeddings, chunk_sources)):
        score = cosine_similarity(query_embed, embed)
        scored_chunks.append((score, chunk, source))
        
    # Sort by score descending
    scored_chunks.sort(key=lambda x: x[0], reverse=True)
    top_k = scored_chunks[:k]
    
    formatted_excerpts = []
    for rank, (score, chunk_text, source) in enumerate(top_k, 1):
        formatted_excerpts.append(f"[Source: {source} | Excerpt {rank} | Similarity: {score:.3f}]\n{chunk_text}")
        
    return "\n\n".join(formatted_excerpts)
