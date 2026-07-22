from fastapi import APIRouter, status
from app.schemas.user import UserCreate

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED
)
def register(user: UserCreate):
    return {
        "message": "User registered successfully"
    }