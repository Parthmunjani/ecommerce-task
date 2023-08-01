from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    # id : int
    name: str
    email: str
    password: str
    phone_number: str = None
    # wallet : float

class UserResponse(BaseModel):
    id : int
    name: str
    email: str
    password: str
    phone_number: str = None
    wallet :Optional[float]  