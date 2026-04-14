from email.mime import image

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, time


# ── Auth
class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class UserOut(BaseModel):
    id: int
    name: str
    email: str
    role: str

    class Config:
        from_attributes = True


# ── Properties
class PropertyCreate(BaseModel):
    title: str
    city: str
    price: float
    type: str
    size: int
    image_url: Optional[str] = None


class PropertyUpdate(BaseModel):
    title: Optional[str] = None
    city: Optional[str] = None
    price: Optional[float] = None
    type: Optional[str] = None
    size: Optional[int] = None
    image_url: Optional[str] = None


class PropertyOut(BaseModel):
    id: int
    title: str
    city: str
    price: float
    type: str
    size: int
    agent_id: int
    image_url: Optional[str] = None

    class Config:
        from_attributes = True


# ── Bookings
class BookingCreate(BaseModel):
    property_id: int
    visit_date: date
    visit_time: time


class BookingOut(BaseModel):
    id: int
    user_id: int
    property_id: int
    visit_date: date
    visit_time: time

    class Config:
        from_attributes = True


# ── Favorites
class FavoriteOut(BaseModel):
    id: int
    user_id: int
    property_id: int

    class Config:
        from_attributes = True
