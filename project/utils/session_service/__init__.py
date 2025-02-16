from typing import TYPE_CHECKING, Optional, Union

from fastapi import HTTPException, status
from project.database.mariadb.models.users import Sessions, Users

if TYPE_CHECKING:
    from project.database.crud import SessionRepository


class SessionService:
    def __init__(self, session_repository: "SessionRepository"):
        self.session_repository = session_repository


    async def get_session(self, token: str) -> Union[HTTPException, Sessions]:
        session = await self.session_repository.get_session(token=token)
        if not session:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
        return session


    async def create_session(self, user: Users, data: dict) -> Union[HTTPException, str]:
        return await self.session_repository.create_session(user=user, data=data)


    async def delete_session(self, token: str) -> Optional[HTTPException]:
        return await self.session_repository.delete_session(token=token)
        