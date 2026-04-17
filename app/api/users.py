from fastapi import Depends , APIRouter

from app.core.security import get_current_user
router = APIRouter(prefix="/users",tags=["Users"])


@router.get("/me")
def get_me(current_user = Depends(get_current_user)):
    return current_user
