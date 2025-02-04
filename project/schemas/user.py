# app/routes/dto/user.py
from pydantic import BaseModel
from typing import Optional


class PersonalDataOut(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    phone_number: Optional[str]

    class Config:
        orm_mode = True


class DeliveryDataOut(BaseModel):
    country: Optional[str]
    city: Optional[str]
    postcode: Optional[str]
    address: Optional[str]

    class Config:
        orm_mode = True


class UserOut(BaseModel):
    user_id: int
    username: str
    email: str
    personal_data: Optional[PersonalDataOut]
    delivery_data: Optional[DeliveryDataOut]

    class Config:
        orm_mode = True
