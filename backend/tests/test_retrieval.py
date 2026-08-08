import pytest
from unittest.mock import patch, MagicMock
from app.core.retrieval import chunk_text, extract_text_from_file

def test_chunk_text():
    text = "word " * 1000
    chunks = chunk_text(text, chunk_size_words=350, overlap_words=50)
    
    # 1000 words with 350 size and 50 overlap:
    # 0-350, 300-650, 600-950, 900-1000 -> 4 chunks
    assert len(chunks) == 4
    assert len(chunks[0].split()) == 350
    assert len(chunks[-1].split()) == 100

def test_extract_text_plain():
    text = b"Hello world"
    extracted = extract_text_from_file("test.txt", text)
    assert extracted == "Hello world"

@pytest.mark.asyncio
@patch('app.core.retrieval.qdrant')
@patch('app.core.retrieval.SessionLocal')
@patch('app.core.retrieval.get_embeddings')
async def test_store_uploaded_document_mocks(mock_get_embeddings, mock_session_local, mock_qdrant):
    # Setup mocks
    mock_get_embeddings.return_value = [[0.1] * 768]
    mock_db = MagicMock()
    mock_session_local.return_value = mock_db
    
    mock_db.query.return_value.filter_by.return_value.first.return_value = None
    
    from app.core.retrieval import store_uploaded_document
    
    result = await store_uploaded_document("test.txt", b"Hello world")
    
    assert result["filename"] == "test.txt"
    assert result["total_chunks"] == 1
    assert result["word_count"] == 2
    
    # Verify DB insertion
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    
    # Verify Qdrant insertion
    mock_qdrant.upsert.assert_called_once()
