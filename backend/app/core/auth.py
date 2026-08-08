import os
import uuid
import bcrypt
import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import settings

security = HTTPBearer()


def hash_password(password: str) -> str:
    """Hash a password using bcrypt directly (passlib is unmaintained and
    incompatible with bcrypt>=4.1)."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its bcrypt hash."""
    try:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
    except ValueError:
        return False

def create_access_token(user_id: str, expires_hours: int = 24) -> str:
    """Create a JWT access token."""
    payload = {
        "sub": user_id,
        "exp": datetime.utcnow() + timedelta(hours=expires_hours)
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm="HS256")

def create_guest_token() -> str:
    """Create a short-lived guest token for anonymous demo access."""
    guest_id = f"guest_{uuid.uuid4().hex[:12]}"
    payload = {
        "sub": guest_id,
        "guest": True,
        "exp": datetime.utcnow() + timedelta(hours=4)
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm="HS256")

async def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    """Verify JWT token from Authorization header."""
    try:
        payload = jwt.decode(credentials.credentials, settings.JWT_SECRET_KEY, algorithms=["HS256"])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
