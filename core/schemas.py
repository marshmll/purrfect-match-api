from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

# USER ============================================================================================
class UserBase(BaseModel):
    name : str
    username : str
    date_birth: date
    datetime_register : datetime
    role : str
    contact_email : Optional[str]
    contact_phone : str

class UserCreate(UserBase):
    password : str

class User(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id : int

# CAT =============================================================================================
class CatBase(BaseModel):
    name : str
    age : int
    sex : str

class CatCreate(CatBase):
    pass

class Cat(CatBase):
    model_config = ConfigDict(from_attributes=True)
    id : int
    
