from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
class Booking(SQLModel, table=True):
    id: Optional[int] = Field(default=None,primary_key=True)
    client_id: int = Field(index=True)
    master_id: int = Field(index=True)
    service_id: int = Field(index=True)
    start_time: datetime
    end_time: datetime
    status: str = Field(default="pending")