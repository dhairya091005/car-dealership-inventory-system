"""Vehicle Pydantic schemas for request validation and response serialization."""

from pydantic import BaseModel, ConfigDict, Field


class VehicleCreate(BaseModel):
    """Schema for creating a new vehicle."""
    make: str
    model: str
    category: str
    price: float = Field(gt=0, description="Price must be positive")
    quantity: int = Field(ge=0, default=0, description="Stock quantity")


class VehicleUpdate(BaseModel):
    """Schema for updating an existing vehicle (all fields optional)."""
    make: str | None = None
    model: str | None = None
    category: str | None = None
    price: float | None = Field(default=None, gt=0)
    quantity: int | None = Field(default=None, ge=0)


class VehicleResponse(BaseModel):
    """Schema for vehicle data returned to the client."""
    id: int
    make: str
    model: str
    category: str
    price: float
    quantity: int

    model_config = ConfigDict(from_attributes=True)


class RestockRequest(BaseModel):
    """Request body for the restock endpoint."""
    quantity: int = Field(gt=0, description="Number of units to add (must be > 0)")
