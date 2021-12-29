import datetime
from pydantic import BaseModel
from sqlalchemy.sql.expression import true


class _UserBase(BaseModel):
    first_name:str
    last_name:str
    email:str


class UserCreate(_UserBase):
    password:str

    class Config:
        orm_mode =True

class User(_UserBase):
    id:int
    is_staff:bool
    date_joined:datetime.datetime

    class Config:
        orm_mode=True


class _CustomerBase(BaseModel):
    names:str
    email:str
    phone_number:str
    business_name:str
    goods_type:str


class CustomerCreate(_CustomerBase):
    secret_code:str

    class Config:
        orm_mode=True


class Customer(_CustomerBase):
    id:int
    agent_id:int

    class Config:
        orm_mode=True

class DimensionBase(BaseModel):
    length:float
    width:float
    weight:int
    maximum_capacity:int

class DimensionCreate(DimensionBase):
    pass

class Dimension(DimensionBase):
    id:int

    class Config:
        orm_mode=True
    



class LocationBase(BaseModel):
    bin_name:str
    row_number:int
    capacity:int



class LocationCreate(LocationBase):
    dimension_id:int
    
    class Config:
        orm_mode=True

class Location(LocationBase):
    id:int
    dimension:Dimension
    availability:bool

    class Config:
        orm_mode=True
    

class Item(BaseModel):
    pass

