from fastapi import FastAPI
from app.database.database import engine

app = FastAPI()

@app.get("/")
def home():
    connection = engine.connect()
    connection.close()
    return {"message": "Database Connected Successfully"}