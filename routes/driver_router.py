from http.client import HTTPException
from typing import List, Annotated
from fastapi import APIRouter, exceptions, WebSocket, WebSocketDisconnect
from fastapi.params import Depends

from config.security import hash_password, require_role
from .Deps.db_session import SessionDep
from models.driver import Driver, DriverCreateIn, DriverCreateOut
from sqlmodel import select
import asyncio

driver_router = APIRouter(tags=['Drivers'],prefix="/drivers")

@driver_router.get("/drivers", response_model=List[DriverCreateOut])
def drivers(db:SessionDep)->List[DriverCreateOut]:
    res = select(Driver).filter(Driver.Driving == True, Driver.active == True)
    driver = db.exec(res).all()
    return [DriverCreateOut(id = d.id, name=d.name, cellphone = d.cellphone, latitude = d.latitude, longitude = d.longitude) for d in driver]

@driver_router.websocket("/get_drivers")
async def get_drivers(websocket: WebSocket, db: SessionDep):
    await websocket.accept()
    try:
        while True:
            statement = select(Driver).where(Driver.Driving == True)
            drivers = db.exec(statement).all()

            drivers_data = [
                {
                    "id": d.id,
                    "name": d.name,
                    "cellphone":d.cellphone,
                    "latitude": d.latitude,
                    "longitude": d.longitude
                }
                for d in drivers
            ]
            await websocket.send_json(drivers_data)
            await asyncio.sleep(2)

    except WebSocketDisconnect:
        print("Cliente desconectado")

@driver_router.post("/create_driver")
def create_driver(db:SessionDep,driver:DriverCreateIn):
    driver_db = Driver(**driver.model_dump())
    driver.password = hash_password(driver.password)
    db.add(driver_db)
    db.commit()
    db.refresh(driver_db)
    return driver_db

@driver_router.put("/activate_deactivate_driver")
def activate_driver(db:SessionDep, id:int):
    D = db.get(Driver,id)
    if not D:
        raise HTTPException(status_code=404, detail="Driver not found")

    if D.active:
        D.active = False
    elif not D.active:
        D.active = True

    db.commit()
    db.refresh(D)
    return D

@driver_router.put("/set_driving")
def set_driving(db:SessionDep, id:int):
    D = db.get(Driver, id)
    if not D:
        raise HTTPException(status_code=404, detail="Driver not found")

    if D.Driving:
        D.Driving = False
    elif not D.Driving:
        D.Driving = True

    db.commit()
    db.refresh(D)
    return D


active_connections = {}


@driver_router.websocket("/driver/position")
async def driver_position(websocket: WebSocket, driver_id: int, db: SessionDep):
    await websocket.accept()
    active_connections[driver_id] = websocket

    try:
        while True:
            data = await websocket.receive_json()
            lat = data.get("latitude")
            lon = data.get("longitude")

            driver = db.get(Driver, driver_id)
            if driver:
                driver.latitude = lat
                driver.longitude = lon
                db.commit()
                db.refresh(driver)

                await websocket.send_json({"status": "position_updated"})

    except WebSocketDisconnect:
        del active_connections[driver_id]


@driver_router.put("/set_calification")
def set_calification(db:SessionDep, id:int, calification:int):
    driver = db.get(Driver, id)
    if not driver:
        raise HTTPException(status_code=404, detail="Deriver not found")
    driver.calification = calification
    db.commit()
    db.refresh(driver)
    return driver