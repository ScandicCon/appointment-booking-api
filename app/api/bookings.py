from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select, Session
from datetime import timedelta, datetime, timezone

from app.schemas.booking import BookingCreate
from app.db.session import get_session
from app.core.security import require_role
from app.models.services import Service
from app.models.booking import Booking

router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.post("/")
def create_booking(booking_data: BookingCreate, session: Session = Depends(get_session), current_user = Depends(require_role(["client"]))):
    service = session.exec(select(Service).where(Service.id == booking_data.service_id)).first()

    if not service:
        raise HTTPException(status_code=404, detail="service not found")
    
    end_time = booking_data.start_time + timedelta(minutes=service.duration_minutes)
    
    conflict_booking = session.exec(select(Booking).where(Booking.master_id == service.master_id, Booking.start_time < end_time, Booking.end_time > booking_data.start_time, Booking.status != 'cancelled')).first()

    if conflict_booking:
        raise HTTPException(status_code=409, detail="Time slot is already booked")
    new_booking = Booking(client_id=current_user.id,master_id=service.master_id, 
                        service_id=service.id,start_time=booking_data.start_time, 
                        end_time=end_time)
    if booking_data.start_time < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Cannot book in the past")

    session.add(new_booking)
    session.commit()
    session.refresh(new_booking)
    return new_booking

@router.get("/me")
def get_my_bookings(current_user = Depends(require_role(["client"])), session: Session = Depends(get_session)):
    my_books = session.exec(select(Booking).where(Booking.client_id == current_user.id)).all()
    return my_books

@router.get("/master")
def get_master_bookings(current_user = Depends(require_role(["master"])), session: Session = Depends(get_session)):
    my_books = session.exec(select(Booking).where(Booking.master_id == current_user.id)).all()
    return my_books

@router.patch("/{booking_id}/status")
def patch_bookind_status(booking_id: int, current_user = Depends(require_role(["master"])) , session: Session = Depends(get_session)):
    find_booking = session.exec(select(Booking).where(Booking.id == booking_id)).first()
    if not find_booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if find_booking.master_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    find_booking.status = "confirmed"
    session.commit()
    session.refresh(find_booking)
    return find_booking