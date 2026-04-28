from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.exceptions import AuthenticationError, ConflictError, ForbiddenError
from app.models.user import User
from app.schemas.auth import TokenResponse


def _normalize_email(email: str) -> str:
    return email.strip().lower()


def register_user(db: Session, *, email: str, password: str) -> User:
    normalized = _normalize_email(email)
    exists = db.scalars(select(User).where(User.email == normalized)).first()
    if exists:
        raise ConflictError("A user with this email already exists")

    user = User(
        email=normalized,
        password_hash=hash_password(password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, *, email: str, password: str) -> TokenResponse:
    normalized = _normalize_email(email)
    user = db.scalars(select(User).where(User.email == normalized)).first()

    if not user or not verify_password(password, user.password_hash):
        raise AuthenticationError("Incorrect email or password")

    if not user.is_active:
        raise ForbiddenError("Inactive user")

    token = create_access_token(subject=user.id, email=user.email)
    return TokenResponse(access_token=token, token_type="bearer")
