from typing import Annotated, Optional

from pydantic import BaseModel, StringConstraints, EmailStr
from .NewUser import MetaData


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
    metadata: MetaData

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "NewUsername",
                    "email": "new_username@example.com",
                    "password": {
                        "old": "old password",
                        "new": "new password"
                    },
                    "metadata": {
                        "os": "IOS",
                        "browser": "Safari",
                        "device": "IPhone 15",
                        "ip": "81.65.35.187"
                    },
                }
            ]
        }
    }
