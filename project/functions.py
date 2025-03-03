import uuid

from project import bearer_scheme
from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from typing import NamedTuple


def generate_unique_file_name(extension) -> str:
    return f"{uuid.uuid4().hex}.{extension}"


class TokenUserData(NamedTuple):
    data: dict
    token: str


async def verify_token(http_authorization: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> TokenUserData:
    from project.utils import TokenService

    token = http_authorization.credentials

    token_service = TokenService()
    token_data = await token_service.verify_token(token)

    if not token_data["token_status"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    return TokenUserData(data=token_data, token=token)
