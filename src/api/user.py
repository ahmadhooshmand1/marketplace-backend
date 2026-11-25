from fastapi import APIRouter, Depends
from psycopg import Connection

from src.connections.db import get_db
from src.schemas.user import (
    LoginRequest,
    LoginResponse,
    UserMeResponse,
    UserUpdate,
    UserUpdateResponse,
)
from src.services import user as user_service
from src.utils.security import get_current_user_id

router = APIRouter(prefix="/v1", tags=["Auth & Users"])


@router.post("/auth/login", response_model=LoginResponse)
def login(body: LoginRequest, db: Connection = Depends(get_db)):
    return user_service.login_or_register(db, body.phone_number)


@router.get("/users/me", response_model=UserMeResponse)
def get_me(
    user_id: int = Depends(get_current_user_id),
    db: Connection = Depends(get_db),
):
    return user_service.get_me(db, user_id)


@router.patch("/users/me", response_model=UserUpdateResponse)
def update_me(
    body: UserUpdate,
    user_id: int = Depends(get_current_user_id),
    db: Connection = Depends(get_db),
):
    return user_service.update_me(db, user_id, body)