import re
import uuid
import hashlib
from typing import List, Dict, Any
from io import BytesIO
from pypdf import PdfReader
from app.core.llm_client import get_embeddings
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from app.models.database import Document, SessionLocal
from app.core.config import settings

# Initialize Qdrant Client
qdrant = QdrantClient(
    url=settings.QDRANT_URL,
    api_key=settings.QDRANT_API_KEY
)

# Ensure collection exists
try:
    qdrant.get_collection("document_chunks")
except Exception:
    try:
        qdrant.create_collection(
            collection_name="document_chunks",
            vectors_config=VectorParams(size=768, distance=Distance.COSINE)
        )
    except Exception:
        pass

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

async def store_uploaded_document(filename: str, file_bytes: bytes) -> Dict[str, Any]:
    """Extracts, chunks, embeds and stores document in PostgreSQL and Qdrant."""
    text = extract_text_from_file(filename, file_bytes)
    
    # Check for duplicate file using hash
    file_hash = hashlib.sha256(file_bytes).hexdigest()
    
    db = SessionLocal()
    try:
        existing = db.query(Document).filter_by(file_hash=file_hash).first()
        if existing:
            # Count existing chunks in Qdrant for this document
            try:
                chunk_count = qdrant.count(
                    collection_name="document_chunks",
                    count_filter={"must": [{"key": "doc_id", "match": {"value": str(existing.id)}}]},
                    exact=True
                ).count
            except Exception:
                chunk_count = 0
            return {
                "file_id": str(existing.id),
                "filename": filename,
                "total_chunks": chunk_count,
                "word_count": existing.word_count or 0,
                "cached": True
            }

        chunks = chunk_text(text)
        embeddings = await get_embeddings(chunks) if chunks else []

        # Store metadata in PostgreSQL
        doc = Document(
            id=uuid.uuid4(),
            filename=filename,
            file_hash=file_hash,
            word_count=len(text.split())
        )
        db.add(doc)
        db.commit()
        db.refresh(doc)
        
        # Store embeddings in Qdrant
        if chunks and embeddings:
            points = [
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=embedding,
                    payload={
                        "doc_id": str(doc.id),
                        "chunk_text": chunk,
                        "filename": filename
                    }
                )
                for chunk, embedding in zip(chunks, embeddings)
            ]
            qdrant.upsert(collection_name="document_chunks", points=points)
            
        return {
            "file_id": str(doc.id),
            "filename": filename,
            "total_chunks": len(chunks),
            "word_count": doc.word_count
        }
    finally:
        db.close()

async def get_top_k_chunks(file_ids: List[str], query: str, k: int = 8) -> str:
    """Retrieves top-k scoring chunks using semantic similarity across multiple documents from Qdrant."""
    if not file_ids:
        return "No document context available."

    # Generate embedding for the user query
    query_embed_list = await get_embeddings([query])
    if not query_embed_list:
        return "Failed to generate query embedding."
    query_embed = query_embed_list[0]
    
    # Search Qdrant for matching chunks
    results = qdrant.search(
        collection_name="document_chunks",
        query_vector=query_embed,
        query_filter={"must": [
            {"key": "doc_id", "match": {"any": file_ids}}
        ]},
        limit=k
    )
    
    if not results:
        return "No relevant context found in the documents."
        
    formatted_excerpts = []
    for rank, result in enumerate(results, 1):
        score = result.score
        chunk_text = result.payload.get("chunk_text", "")
        source = result.payload.get("filename", "Unknown")
        formatted_excerpts.append(f"[Source: {source} | Excerpt {rank} | Similarity: {score:.3f}]\n{chunk_text}")
        
    return "\n\n".join(formatted_excerpts)
