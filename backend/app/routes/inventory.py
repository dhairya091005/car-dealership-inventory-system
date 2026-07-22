"""
Inventory router — purchase and restock endpoints.

  POST /api/vehicles/:id/purchase  — Buy one unit (quantity -= 1). Protected.
  POST /api/vehicles/:id/restock   — Add stock units. Admin only.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user, require_admin
from app.database.dependencies import get_db
from app.models.user import User
from app.models.vehicle import Vehicle
from app.schemas.vehicle import RestockRequest, VehicleResponse

router = APIRouter(prefix="/api/vehicles", tags=["Inventory"])


@router.post("/{vehicle_id}/purchase", response_model=VehicleResponse)
def purchase_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Purchase one unit of a vehicle.
    Decreases quantity by 1. Returns 400 if out of stock.
    """
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()

    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vehicle with id {vehicle_id} not found",
        )

    if vehicle.quantity == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Vehicle '{vehicle.make} {vehicle.model}' is out of stock",
        )

    vehicle.quantity -= 1
    db.commit()
    db.refresh(vehicle)
    return vehicle


@router.post("/{vehicle_id}/restock", response_model=VehicleResponse)
def restock_vehicle(
    vehicle_id: int,
    body: RestockRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """
    Restock a vehicle by adding units to its quantity.
    Admin only. Returns 404 if vehicle not found.
    """
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()

    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vehicle with id {vehicle_id} not found",
        )

    vehicle.quantity += body.quantity
    db.commit()
    db.refresh(vehicle)
    return vehicle
