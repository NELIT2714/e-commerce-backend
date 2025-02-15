from pydantic import BaseModel, field_serializer
from typing import Optional
from datetime import datetime


class PersonalDataOut(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    phone_number: Optional[str]

    class Config:
        from_attributes = True


class DeliveryDataOut(BaseModel):
    country: Optional[str]
    city: Optional[str]
    postcode: Optional[str]
    address: Optional[str]

    class Config:
        from_attributes = True


class SessionOut(BaseModel):
    session_id: int
    user_id: int
    token: str
    created_at: datetime

    @field_serializer("created_at")
    def serialize_created_at(self, value: datetime):
        return datetime.strftime(value, "%Y-%m-%d %H:%M:%S")

    class Config:
        from_attributes = True


class UserOut(BaseModel):
    user_id: int
    username: str
    email: str
    sessions: Optional[list[SessionOut]]
    personal_data: Optional[PersonalDataOut]
    delivery_data: Optional[DeliveryDataOut]

    class Config:
        from_attributes = True
