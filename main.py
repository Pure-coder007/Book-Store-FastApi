from fastapi import FastAPI
from .database import Base
import uvicorn



app = FastAPI()


@app.get("/")
def index():
    return {"message": "Hello World"}