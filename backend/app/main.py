from fastapi import FastAPI

from app.database.database import Base, engine
from app.routes.auth import router as auth_router
from app.routes.vehicles import router as vehicles_router

# Import all models so SQLAlchemy registers them before create_all
import app.models.user   # noqa: F401
import app.models.vehicle  # noqa: F401

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Car Dealership Inventory API", version="1.0.0")


@app.get("/")
def root():
    return {"message": "Car Dealership Inventory API is running"}


app.include_router(auth_router)
app.include_router(vehicles_router)
