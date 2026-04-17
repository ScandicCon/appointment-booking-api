from sqlmodel import SQLModel
from typing import Optional


class ServiceCreate(SQLModel):
    title: str
    description: Optional[str] = None
    duration_minutes: int
    price: float