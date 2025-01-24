from pydantic import BaseModel, field_validator, model_validator, constr, EmailStr
from typing import List, Literal
from fastapi.exceptions import HTTPException

Permissions = Literal[
    "add_admins",
    "delete_admins",
    "edit_admins",
    "view_contact_forms",
    "delete_contact_forms",
    "add_articles",
    "delete_articles",
    "edit_articles",
    "*"
]


class NewAdmin(BaseModel):
    username: constr(min_length=2, max_length=30)
    email: EmailStr
    permissions: List[Permissions]
    password: constr(min_length=8, max_length=32)
    repeated_password: constr(min_length=8, max_length=32)

    @model_validator(mode="before")
    def check_passwords_match(cls, values):
        password = values.get("password")
        repeated_password = values.get("repeated_password")

        if not password == repeated_password:
            raise HTTPException(status_code=400, detail="Passwords do not match")
        return values

    @field_validator("permissions", mode="before")
    def validate_unique_permissions(cls, value):
        if not len(value) == len(set(value)):
            raise ValueError("Permissions must not contain duplicates")
        return value
