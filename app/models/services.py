from sqlmodel import SQLModel, Field
from typing import Optional

class Service(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str 
    description: Optional[str] = Field(default=None)
    duration_minutes: int
    price: float
    is_active: bool = Field(default=True)
    master_id: int = Field(index=True)