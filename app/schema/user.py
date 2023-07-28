from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    phone_number: str = None
