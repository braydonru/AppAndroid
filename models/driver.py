from typing import Optional

from sqlmodel import SQLModel, Field


class Driver(SQLModel, table=True):
    id:Optional[int] = Field(default=None, primary_key=True)
    name:str = Field(default=None)
    cellphone:str = Field(default=None)
    password:str = Field(default=None)
    active: bool = Field(default=False)
    Driving: bool = Field(default=False)
    longitude: float = Field(default=None)
    latitude: float = Field(default=None)
    admin: bool = Field(default=False)
