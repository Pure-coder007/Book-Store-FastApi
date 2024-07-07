from fastapi import FastAPI
from database import Base, engine
import models
import uvicorn
from routers import users, authentication, books



app = FastAPI()

models.Base.metadata.create_all(bind=engine)
print("Database created.....")

app.include_router(users.router)
app.include_router(authentication.router)
app.include_router(books.router)