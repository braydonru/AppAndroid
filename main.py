from fastapi import FastAPI
from config.db import engine
from sqlmodel import SQLModel

from config.security import security
from models import *
from routes.driver_router import driver_router
from fastapi.middleware.cors import CORSMiddleware

SQLModel.metadata.create_all(engine)
app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/",tags=["Main"])
async def root():
    return {"message": "UberApp Backend"}

app.include_router(driver_router)
app.include_router(security)