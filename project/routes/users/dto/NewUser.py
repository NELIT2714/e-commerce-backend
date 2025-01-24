from fastapi.exceptions import HTTPException
from pydantic import BaseModel, constr, EmailStr, model_validator


class NewUser(BaseModel):
    username: constr(min_length=2, max_length=30)
    email: EmailStr
    password: constr(min_length=8, max_length=32)
    repeated_password: constr(min_length=8, max_length=32)

    @model_validator(mode="before")
    def check_passwords_match(cls, values):
        password = values.get("password")
        repeated_password = values.get("repeated_password")

        if not password == repeated_password:
            raise HTTPException(status_code=400, detail="Passwords do not match")
        return values
