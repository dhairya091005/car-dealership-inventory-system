from fastapi import FastAPI

from app.database.database import Base, engine
from app.routes.auth import router as auth_router
from app.routes.vehicles import router as vehicles_router
from app.routes.inventory import router as inventory_router
from app.routes.admin import router as admin_router

# Import all models so SQLAlchemy registers them before create_all
import app.models.user   # noqa: F401
import app.models.vehicle  # noqa: F401

Base.metadata.create_all(bind=engine)

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    On startup, check if FIRST_ADMIN_EMAIL is set in the environment.
    If so, promote that user to ADMIN if they exist.
    This ensures there is always a way to get the first admin into the system.
    """
    import os
    from sqlalchemy.orm import Session
    from app.database.database import SessionLocal
    from app.models.user import User

    first_admin_email = os.getenv("FIRST_ADMIN_EMAIL")
    if first_admin_email:
        db: Session = SessionLocal()
        try:
            user = db.query(User).filter(User.email == first_admin_email).first()
            if user and user.role != "ADMIN":
                user.role = "ADMIN"
                db.commit()
                print(f"[startup] Promoted {first_admin_email} to ADMIN.")
        finally:
            db.close()
    
    yield

app = FastAPI(title="Car Dealership Inventory API", version="1.0.0", lifespan=lifespan)

@app.get("/")
def root():
    return {"message": "Car Dealership Inventory API is running"}



app.include_router(auth_router)
app.include_router(vehicles_router)
app.include_router(inventory_router)
app.include_router(admin_router)
