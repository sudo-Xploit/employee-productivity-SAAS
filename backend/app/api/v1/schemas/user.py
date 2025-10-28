from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = True


class UserCreate(UserBase):
    email: EmailStr
    password: str = Field(..., min_length=8)


class UserUpdate(UserBase):
    password: Optional[str] = Field(None, min_length=8)


class UserInDBBase(UserBase):
    id: Optional[int] = None
    role: str

    class Config:
        from_attributes = True


class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    hashed_password: str