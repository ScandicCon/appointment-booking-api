from sqlmodel import SQLModel
from datetime import datetime


class BookingCreate(SQLModel):
    service_id: int
    start_time: datetime