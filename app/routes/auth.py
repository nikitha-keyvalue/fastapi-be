from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.controllers import auth as ctrl
from app.deps import get_db
from app.schemas.auth import LoginRequest, TokenResponse, UserPublic, UserRegisterRequest

router = APIRouter()


@router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def register(payload: UserRegisterRequest, db: Session = Depends(get_db)):
    return ctrl.register(payload, db)


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    return ctrl.login(payload, db)
