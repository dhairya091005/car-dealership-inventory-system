from fastapi import FastAPI
from app.database.database import Base, engine
from app.routes.auth import router as auth_router

import app.models

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API Running"}

app.include_router(auth_router)
