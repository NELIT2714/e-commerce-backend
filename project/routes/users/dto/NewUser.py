from typing import Annotated
from fastapi.exceptions import HTTPException
from pydantic import BaseModel, StringConstraints, EmailStr, model_validator


class MetaData(BaseModel):
    os: Annotated[str, StringConstraints(max_length=50)]
    browser: Annotated[str, StringConstraints(max_length=50)]
    device: Annotated[str, StringConstraints(max_length=100)]
    ip: Annotated[str, StringConstraints(max_length=20)]


class NewUser(BaseModel):
    username: Annotated[str, StringConstraints(min_length=2, max_length=30)]
    email: EmailStr
    metadata: MetaData
    password: Annotated[str, StringConstraints(min_length=8, max_length=32)]
    repeated_password: Annotated[str, StringConstraints(min_length=8, max_length=32)]

    @model_validator(mode="before")
    def check_passwords_match(cls, values):
        password = values.get("password")
        repeated_password = values.get("repeated_password")

        if not password == repeated_password:
            raise HTTPException(status_code=400, detail="Passwords do not match")
        return values
        
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "ExampleUsername",
                    "email": "example@domain.com",
                    "metadata": {
                        "os": "IOS",
                        "browser": "Safari",
                        "device": "IPhone 15",
                        "ip": "81.65.35.187"
                    },
                    "password": "Qwerty123_@",
                    "repeated_password": "Qwerty123_@"
                }
            ]
        }
    }
