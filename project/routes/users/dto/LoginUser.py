from pydantic import BaseModel

from project.routes.users.dto.NewUser import MetaData


class LoginUser(BaseModel):
    username: str
    password: str
    metadata: MetaData

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "ExampleUsername",
                    "password": "Qwerty123_@",
                    "metadata": {
                        "os": "IOS",
                        "browser": "Safari",
                        "device": "IPhone 15",
                        "ip": "81.65.35.187"
                    }
                }
            ]
        }
    }
