from pydantic import BaseModel


class LoginAdmin(BaseModel):
    username_or_email: str
    password: str
