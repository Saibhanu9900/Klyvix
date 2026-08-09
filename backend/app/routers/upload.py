from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from typing import List
import magic
from app.core.retrieval import store_uploaded_document
from app.models.schemas import DocumentUploadResponse
from app.core.auth import verify_token
from app.core.rate_limit import upload_limiter

router = APIRouter(prefix="/api", tags=["upload"])

ALLOWED_MIME_TYPES = ["application/pdf"]
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

@router.post("/upload", response_model=List[DocumentUploadResponse], dependencies=[Depends(verify_token), Depends(upload_limiter)])
async def upload_document(files: List[UploadFile] = File(...)):
    """Uploads multiple PDF documents, extracts text, chunks them, and stores them in memory."""
    responses = []
    for file in files:
            
        try:
            contents = await file.read()
            if len(contents) > MAX_FILE_SIZE:
                raise HTTPException(status_code=400, detail=f"File {file.filename} exceeds 10MB limit.")
                
            mime_type = magic.from_buffer(contents, mime=True)
            if mime_type not in ALLOWED_MIME_TYPES:
                raise HTTPException(status_code=400, detail=f"Invalid file type: {mime_type}")
                
            try:
                import pypdf
                import io
                reader = pypdf.PdfReader(io.BytesIO(contents))
                if reader.is_encrypted:
                    raise HTTPException(status_code=400, detail=f"File {file.filename} is encrypted.")
                _ = len(reader.pages)
            except HTTPException:
                raise
            except Exception:
                raise HTTPException(status_code=400, detail=f"Corrupted or invalid PDF {file.filename}.")
                
            result = await store_uploaded_document(file.filename, contents)
            responses.append(DocumentUploadResponse(**result))
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to process PDF {file.filename}: {str(e)}")
            
    return responses
