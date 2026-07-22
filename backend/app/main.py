from fastapi import FastAPI
from app.database.database import Base, engine

import app.models

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API Running"}