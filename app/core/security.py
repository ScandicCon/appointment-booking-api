from datetime import datetime, timedelta, timezone
import jwt
from pwdlib import PasswordHash
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from sqlmodel import Session, select

from app.core.config import SECRET_KEY, ACCESS_TOKEN_EXPIRE, ALGORITHM
from app.models.user import User
from app.db.session import get_session

password_hasher = PasswordHash.recommended()

DUMMY_HASH  = password_hasher.hash("DUMMY_PASSWORD")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=("token"))

def hash_password(password: str):
    return password_hasher.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return password_hasher.verify(plain_password, hashed_password)

def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(ACCESS_TOKEN_EXPIRE)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(session: Session = Depends(get_session), token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload.get("sub")
    user = session.exec(select(User).where(User.id == user_id)).first()
    if not user:
        raise HTTPException(status_code=401)
    return user

def require_role(role: list):
    def checker(current_user = Depends(get_current_user)):
        if current_user.role in role:
            return current_user
        else:
            raise HTTPException(status_code=403)
    return checker