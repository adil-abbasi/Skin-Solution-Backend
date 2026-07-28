from pydantic import BaseModel
from typing import Optional



class UserLogin(BaseModel):

    username: str
    password: str



class ChangePassword(BaseModel):

    old_password: str
    new_password: str



class UserCreate(BaseModel):

    username: str
    password: str
    full_name: str
    role: str = "Receptionist"



class UserUpdate(BaseModel):

    username: Optional[str] = None
    full_name: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None



class UserResponse(BaseModel):

    id: int
    username: str
    full_name: str
    role: str
    is_active: bool


    class Config:
        from_attributes = True