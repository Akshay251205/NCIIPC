"""Password-based supervisor authentication for the SAT-SA web client."""
from datetime import datetime, timedelta, timezone
import base64
import hashlib
import hmac
import re
import secrets

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, Field
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import AuthSession, SupervisorUser

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])

USERNAME = re.compile(r"^[A-Za-z0-9_.-]{3,64}$")
EMAIL = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
SESSION_DAYS = 7


class SignUpRequest(BaseModel):
    username: str = Field(min_length=3, max_length=64)
    email: str = Field(min_length=3, max_length=254)
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    identity: str = Field(min_length=3, max_length=254)
    password: str = Field(min_length=1, max_length=128)


def hash_password(password: str, salt: bytes | None = None) -> str:
    salt = salt or secrets.token_bytes(16)
    digest = hashlib.scrypt(password.encode("utf-8"), salt=salt, n=2**14, r=8, p=1)
    return f"scrypt${base64.b64encode(salt).decode()}${base64.b64encode(digest).decode()}"


def verify_password(password: str, encoded: str) -> bool:
    try:
        _, salt_value, digest_value = encoded.split("$", 2)
        salt = base64.b64decode(salt_value)
        expected = base64.b64decode(digest_value)
        actual = hashlib.scrypt(password.encode("utf-8"), salt=salt, n=2**14, r=8, p=1)
        return hmac.compare_digest(actual, expected)
    except (ValueError, TypeError):
        return False


def profile(user: SupervisorUser) -> dict[str, str]:
    return {"username": user.username, "email": user.email}


def create_session(db: Session, user: SupervisorUser) -> str:
    token = secrets.token_urlsafe(32)
    db.add(AuthSession(
        user_id=user.id,
        token_hash=hashlib.sha256(token.encode()).hexdigest(),
        expires_at=datetime.now(timezone.utc) + timedelta(days=SESSION_DAYS),
    ))
    db.commit()
    return token


def get_current_session(request: Request, db: Session) -> tuple[AuthSession, SupervisorUser]:
    authorization = request.headers.get("Authorization", "")
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required.")
    token_hash = hashlib.sha256(authorization.removeprefix("Bearer ").encode()).hexdigest()
    session = db.query(AuthSession).filter(AuthSession.token_hash == token_hash).first()
    if not session or session.expires_at.replace(tzinfo=timezone.utc) <= datetime.now(timezone.utc):
        if session:
            db.delete(session)
            db.commit()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Your session has expired. Please sign in again.")
    user = db.get(SupervisorUser, session.user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required.")
    return session, user


@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(payload: SignUpRequest, db: Session = Depends(get_db)):
    username, email = payload.username.strip(), payload.email.strip().lower()
    if not USERNAME.fullmatch(username):
        raise HTTPException(status_code=422, detail="Username must use 3–64 letters, numbers, dots, hyphens, or underscores.")
    if not EMAIL.fullmatch(email):
        raise HTTPException(status_code=422, detail="Enter a valid email address.")
    if db.query(SupervisorUser).filter(or_(SupervisorUser.username == username, SupervisorUser.email == email)).first():
        raise HTTPException(status_code=409, detail="That username or email is already registered.")
    user = SupervisorUser(username=username, email=email, password_hash=hash_password(payload.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"token": create_session(db, user), "user": profile(user)}


@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    identity = payload.identity.strip()
    user = db.query(SupervisorUser).filter(or_(SupervisorUser.username == identity, SupervisorUser.email == identity.lower())).first()
    if not user:
        raise HTTPException(status_code=401, detail="No SAT-SA account is registered for that email or username.")
    if not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect password. Please try again.")
    return {"token": create_session(db, user), "user": profile(user)}


@router.get("/me")
def me(request: Request, db: Session = Depends(get_db)):
    _, user = get_current_session(request, db)
    return {"user": profile(user)}


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(request: Request, db: Session = Depends(get_db)):
    session, _ = get_current_session(request, db)
    db.delete(session)
    db.commit()
