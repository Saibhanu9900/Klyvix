from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from app.core.auth import create_access_token, create_guest_token, hash_password, verify_password
from app.models.database import SessionLocal, User

router = APIRouter(prefix="/api/auth", tags=["auth"])

class AuthRequest(BaseModel):
    email: str
    password: str

@router.post("/register")
def register(request: AuthRequest):
    """Register a new user with bcrypt-hashed password stored in Postgres."""
    db = SessionLocal()
    try:
        existing = db.query(User).filter_by(email=request.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="User already exists")
        
        import uuid
        user = User(
            id=uuid.uuid4(),
            email=request.email,
            hashed_password=hash_password(request.password)
        )
        db.add(user)
        db.commit()
        
        token = create_access_token(request.email)
        return {"access_token": token, "token_type": "bearer"}
    finally:
        db.close()

@router.post("/login")
def login(request: AuthRequest):
    """Authenticate user with bcrypt password verification."""
    db = SessionLocal()
    try:
        user = db.query(User).filter_by(email=request.email).first()
        if not user or not verify_password(request.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        token = create_access_token(request.email)
        return {"access_token": token, "token_type": "bearer"}
    finally:
        db.close()

@router.post("/guest")
def guest_access():
    """Issue a short-lived guest token for anonymous demo access.
    No password, no registration — just a 4-hour session token."""
    token = create_guest_token()
    return {"access_token": token, "token_type": "bearer", "guest": True}
