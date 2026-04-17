from http.client import HTTPException

from fastapi import APIRouter, exceptions
from config.security import hash_password
from .Deps.db_session import SessionDep
from models.driver import Driver
from sqlmodel import select


driver_router = APIRouter(tags=['Drivers'],prefix="/drivers")

@driver_router.get("/get_drivers")
def get_drivers(db:SessionDep):
    res = select(Driver)
    drivers = db.exec(res).all()
    return drivers

@driver_router.post("/create_driver")
def create_driver(driver:Driver,db:SessionDep):
    D = Driver(**driver.model_dump())
    D.password = hash_password(driver.password)
    db.add(D)
    db.commit()
    db.refresh(D)
    return D

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


@driver_router.put("/modify_position")
def modify_position(db:SessionDep, lat:float,lon:float,id:int):
    D = db.get(Driver, id)
    if not D:
        raise exceptions.HTTPException(status_code=404, detail="Driver not found")
    D.latitude = lat
    D.longitude = lon
    db.commit()
    db.refresh(D)
    return D
