from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from app.core.retrieval import store_uploaded_document
from app.models.schemas import DocumentUploadResponse

router = APIRouter(prefix="/api", tags=["upload"])

@router.post("/upload", response_model=List[DocumentUploadResponse])
async def upload_document(files: List[UploadFile] = File(...)):
    """Uploads multiple PDF documents, extracts text, chunks them, and stores them in memory."""
    responses = []
    for file in files:
            
        try:
            contents = await file.read()
            if len(contents) > 10 * 1024 * 1024: # 10MB size limit
                raise HTTPException(status_code=400, detail=f"File {file.filename} exceeds 10MB limit.")
                
            result = await store_uploaded_document(file.filename, contents)
            responses.append(DocumentUploadResponse(**result))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to process PDF {file.filename}: {str(e)}")
            
    return responses
