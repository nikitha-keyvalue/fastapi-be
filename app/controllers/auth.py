from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.exceptions import AuthenticationError, ConflictError, ForbiddenError
from app.models.user import User
from app.schemas.auth import LoginRequest, TokenResponse, UserRegisterRequest
from app.services import auth_service


def register(payload: UserRegisterRequest, db: Session) -> User:
    try:
        return auth_service.register_user(
            db, email=str(payload.email), password=payload.password,
        )
    except ConflictError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=exc.detail,
        ) from exc


def login(payload: LoginRequest, db: Session) -> TokenResponse:
    try:
        return auth_service.authenticate_user(
            db, email=str(payload.email), password=payload.password,
        )
    except AuthenticationError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=exc.detail,
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
    except ForbiddenError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=exc.detail,
        ) from exc
