from pydantic import BaseModel

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
    # wallet : float