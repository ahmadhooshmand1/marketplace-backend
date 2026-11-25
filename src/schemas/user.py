from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    phone_number: str = Field(pattern=r"^09\d{9}$")


class UserLoginInfo(BaseModel):
    id: int
    full_name: str
    phone_number: str
    has_booth: bool


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserLoginInfo


class UserMeResponse(BaseModel):
    id: int
    full_name: str
    phone_number: str
    email: EmailStr | None = None
    has_booth: bool
    created_at: datetime


class UserUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=2, max_length=100)
    email: EmailStr | None = None


class UserUpdateResponse(BaseModel):
    id: int
    full_name: str
    phone_number: str
    email: EmailStr | None = None