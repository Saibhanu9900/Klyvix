from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.auth import create_access_token

router = APIRouter(prefix="/api/auth", tags=["auth"])

class AuthRequest(BaseModel):
    email: str
    password: str

# Mock user database for Phase 1
MOCK_USERS = {}

@router.post("/register")
def register(request: AuthRequest):
    if request.email in MOCK_USERS:
        raise HTTPException(status_code=400, detail="User already exists")
    MOCK_USERS[request.email] = request.password
    token = create_access_token(request.email)
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login")
def login(request: AuthRequest):
    if request.email not in MOCK_USERS or MOCK_USERS[request.email] != request.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(request.email)
    return {"access_token": token, "token_type": "bearer"}
