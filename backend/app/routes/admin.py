"""
Admin router — user management for administrators.

Endpoints:
  POST /api/admin/promote-user  — promote a user to ADMIN role (admin only)
  GET  /api/admin/users         — list all users (admin only)
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from app.auth.dependencies import require_admin
from app.database.dependencies import get_db
from app.models.user import User

router = APIRouter(prefix="/api/admin", tags=["Admin"])


class PromoteRequest(BaseModel):
    """Request body for promoting a user to ADMIN."""
    email: EmailStr


class UserAdminResponse(BaseModel):
    """Response schema for user data in admin context."""
    id: int
    username: str
    email: str
    role: str

    class Config:
        from_attributes = True


@router.post("/promote-user", response_model=UserAdminResponse)
def promote_user(
    body: PromoteRequest,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """
    Promote a user to the ADMIN role by email address.
    Idempotent — promoting an existing admin returns 200 with no error.
    Admin access required.
    """
    user = db.query(User).filter(User.email == body.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No user found with email '{body.email}'",
        )

    user.role = "ADMIN"
    db.commit()
    db.refresh(user)
    return user


@router.get("/users", response_model=list[UserAdminResponse])
def list_users(
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """List all registered users. Admin access required."""
    return db.query(User).all()
