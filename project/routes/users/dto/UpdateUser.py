from typing import Optional

from pydantic import BaseModel, constr, EmailStr


class PersonalData(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None


class DeliveryData(BaseModel):
    country: Optional[str] = None
    city: Optional[str] = None
    postcode: Optional[str] = None
    address: Optional[str] = None


class Password(BaseModel):
    old: Optional[constr(min_length=8, max_length=32)] = None
    new: Optional[constr(min_length=8, max_length=32)] = None


class UpdateUser(BaseModel):
    username: Optional[constr(min_length=2, max_length=30)] = None
    email: Optional[EmailStr] = None
    personal_data: Optional[PersonalData] = None
    delivery_data: Optional[DeliveryData] = None
    password: Optional[Password] = None
