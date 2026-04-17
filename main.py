from fastapi import FastAPI
from config.db import engine
from sqlmodel import SQLModel
from models import *
from routes.driver_router import driver_router

SQLModel.metadata.create_all(engine)
app = FastAPI()


@app.get("/",tags=["Main"])
async def root():
    return {"message": "Hello World"}

app.include_router(driver_router)
