from typing import Annotated, Optional

from pydantic import BaseModel, StringConstraints, constr, EmailStr


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
    old: Optional[Annotated[str, StringConstraints(min_length=8, max_length=32)]] = None
    new: Optional[Annotated[str, StringConstraints(min_length=8, max_length=32)]] = None


class UpdateUser(BaseModel):
    username: Optional[Annotated[str, StringConstraints(min_length=2, max_length=30)]] = None
    email: Optional[EmailStr] = None
    password: Optional[Password] = None
