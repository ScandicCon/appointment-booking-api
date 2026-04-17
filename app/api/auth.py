from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select


from app.db.session import get_session
from app.schemas.user import UserCreate, UserRead, UserLogin
from app.models.user import User
from app.core.security import hash_password, verify_password, DUMMY_HASH, create_token


router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserRead)
def register(user_data: UserCreate, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == user_data.email)).first()
    if user:
        raise HTTPException(status_code=409, detail="User with this email already exists")
    hash=hash_password(user_data.password)
    new_user = User(email=user_data.email,username=user_data.username,hashed_password=hash)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

@router.post("/login")
def login(user_data: UserLogin, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == user_data.email)).first()

    if not user:
        verify_password(user_data.password, DUMMY_HASH)
        raise HTTPException(status_code=401, detail="Invalid email or password")
    if not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    access_token = create_token({"sub": str(user.id)})
    return {
        "access_token":access_token,
        "token_type": "bearer"
    }