from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class UserBase(BaseModel):
    name : str
    username : str
    date_birth: date
    datetime_register : datetime
    role : str
    contact_email : Optional[str]
    contact_phone : str

class UserCreate(UserBase):
    pass_hash : str

class User(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id : int
    
