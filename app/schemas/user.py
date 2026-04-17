from sqlmodel import SQLModel
from pydantic import EmailStr


class UserCreate(SQLModel):
    email: EmailStr
    username: str
    password: str


class UserRead(SQLModel):
    id: int
    email: EmailStr
    username: str
    role: str
    is_active: bool


class UserLogin(SQLModel):
    email: EmailStr
    password: str