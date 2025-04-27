from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr
    phone: Optional[str] = Field(None, regex=r'^\+?[1-9]\d{1,14}$') 
    address: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None

class UserCreate(UserBase):
    password: str
    role: str = 'user'

class UserUpdate(UserBase):
    password: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None

class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True