from typing import Optional

from sqlmodel import SQLModel, Field


class Driver(SQLModel, table=True):
    id:Optional[int] = Field(default=None, primary_key=True)
    name:str = Field(default=None)
    cellphone:str = Field(default=None, unique=True)
    password:str = Field(default=None)
    active: Optional[bool]  = Field(default=False)
    Driving: Optional[bool] = Field(default=False)
    longitude: Optional[float] = Field(default=0.0)
    latitude: Optional[float] = Field(default=0.0)
    admin: Optional[bool] = Field(default=False)
    calification: Optional[int] = Field(default=1, ge=1, le=5)

class DriverCreateIn(SQLModel):
    name: str = Field(default=None)
    cellphone: str = Field(default=None, unique=True)
    password: str = Field(default=None)

class DriverCreateOut(SQLModel):
    id: int = Field(default=None)
    name: str = Field(default=None)
    cellphone: str = Field(default=None, unique=True)
    longitude: Optional[float] = Field(default=0.0)
    latitude: Optional[float] = Field(default=0.0)