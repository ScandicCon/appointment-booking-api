from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.db.session import get_session
from app.core.security import require_role

from app.schemas.service import ServiceCreate
from app.models.services import Service

router = APIRouter(prefix="/services", tags=["Services"])

@router.post("/")
def create_service(service_data: ServiceCreate ,session: Session = Depends(get_session),
    current_user = Depends(require_role(["master"]))):
    
    new_service = Service(
        title=service_data.title,
        description=service_data.description,
        duration_minutes=service_data.duration_minutes,
        price=service_data.price,
        master_id=current_user.id
    )
    session.add(new_service)
    session.commit()
    session.refresh(new_service)
    return new_service

@router.get("/")
def get_services(session: Session = Depends(get_session)):
    services = session.exec(select(Service)).all()
    return services

@router.get("/me")
def get_me(current_user = Depends(require_role(["master"])), session: Session = Depends(get_session)):
    services = session.exec(select(Service).where(Service.master_id == current_user.id)).all()
    return services 