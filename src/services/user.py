from fastapi import HTTPException, status
from psycopg import Connection

from src.repositories import user as user_repo
from src.schemas.user import UserUpdate
from src.utils.security import create_access_token


def login_or_register(db: Connection, phone_number: str) -> dict:
    user = user_repo.get_user_by_phone(db, phone_number)
    if not user:
        user = user_repo.create_user_by_phone(db, phone_number)

    token = create_access_token(user["id"])
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": user,
    }


def get_me(db: Connection, user_id: int) -> dict:
    user = user_repo.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or invalid token.",
        )
    return user


def update_me(db: Connection, user_id: int, data: UserUpdate) -> dict:
    if data.email is not None:
        existing = user_repo.get_user_by_email(db, data.email)
        if existing and existing["id"] != user_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email is already registered.",
            )

    updated_user = user_repo.update_user(db, user_id, data.full_name, data.email)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )
    return updated_user