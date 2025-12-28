from pydantic import BaseModel
from typing import Literal

class UserCreate(BaseModel):
    name: str
    email : str
    password : str
    role: str
class UserResponse(BaseModel):
    id: int
    name: str
    email : str
    role : str

    class Config:
        from_attributes = True
class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    password: str | None = None
    role: Literal["admin", "user"] | None = None
