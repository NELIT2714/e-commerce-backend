import os
import jwt
import datetime

from abc import ABC, abstractmethod


class TokenConfig:
    SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    ALGORITHM = os.getenv("JWT_ALGORITHM")
    DEFAULT_TTL = int(os.getenv("JWT_DEFAULT_TTL"))


class ITokenService(ABC):
    @abstractmethod
    async def generate_token(self, ttl: int = TokenConfig.DEFAULT_TTL, **kwargs) -> str:
        pass

    @abstractmethod
    async def verify_token(self, token: str) -> dict:
        pass


class TokenService:
    def __init__(self):
        pass

    async def generate_token(self, ttl: int = TokenConfig.DEFAULT_TTL, **kwargs) -> str:
        payload = {
            "exp": int(datetime.datetime.now().timestamp()) + (ttl * 60) * 60,
            **kwargs
        }
        # payload.update(kwargs)

        token = jwt.encode(payload, TokenConfig.SECRET_KEY, algorithm=TokenConfig.ALGORITHM)
        return token

    async def verify_token(self, token: str):
        try:
            decoded_data = jwt.decode(token, TokenConfig.SECRET_KEY, algorithms=[TokenConfig.ALGORITHM])
            expiration_time = decoded_data["exp"]
            decoded_data.pop("exp", None)

            return {
                "token_status": True,
                "token_data": {
                    **decoded_data,
                },
                "expiration_time": expiration_time
            }
        except jwt.ExpiredSignatureError:
            return {"token_status": False, "detail": "Token expired"}
        except jwt.InvalidTokenError:
            return {"token_status": False, "detail": "Invalid token"}
        
    # async def check_token(self, token: str):

        