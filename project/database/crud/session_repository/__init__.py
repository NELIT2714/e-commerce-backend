import asyncio
import datetime

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional, Union

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload
from pymysql import err
from fastapi import HTTPException, status

from project import logger
from project.database.mariadb.models.users import Sessions, SessionsData, Users

from project.utils import TokenService

if TYPE_CHECKING:
    from project.utils import SessionDBManager


class ISessionRepository(ABC):
    @abstractmethod
    async def get_session(self, token: str) -> Union[HTTPException, Sessions]:
        pass

    @abstractmethod
    async def create_session(self, user: Users, data: dict) -> Union[HTTPException, str]:
        pass

    @abstractmethod
    async def delete_session(self, token: str) -> Optional[HTTPException]:
        pass


class SessionRepository(ISessionRepository):
    def __init__(self, session_db_manager: "SessionDBManager"):
        self._session_db_manager = session_db_manager


    async def get_session(self, token: str) -> Union[HTTPException, Sessions]:
        session_db = await self._session_db_manager.get_session()
        
        try:
            user_session_query = await session_db.execute(select(Sessions).options(selectinload(Sessions.data)).filter_by(token=token))
            return user_session_query.scalar_one_or_none()
        except (err.MySQLError, SQLAlchemyError) as e:
            await session_db.rollback()
            logger.error(f"Database error: {e}")
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            await self._session_db_manager.close_session()


    async def create_session(self, user: Users, data: dict) -> Union[HTTPException, str]:
        session_db = await self._session_db_manager.get_session()
        
        try:
            token_service = TokenService()
            token = await token_service.generate_token(user_id=user.user_id)

            session = Sessions(
                user_id=user.user_id,
                token=token,
                created_at=datetime.datetime.now()
            )
            session_db.add(session)
            await session_db.flush()

            session_db.add(SessionsData(
                session_id=session.session_id,
                os=data["os"],
                browser=data["browser"],
                device=data["device"],
                ip=data["ip"]
            ))
            await session_db.commit()

            return token
        except (err.MySQLError, SQLAlchemyError) as e:
            await session_db.rollback()
            logger.error(f"Database error: {e}")
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            await self._session_db_manager.close_session()


    async def delete_session(self, token: str) -> Optional[HTTPException]:
        if not (user_session := await self.get_session(token=token)):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")

        session_db = await self._session_db_manager.get_session()
        try:
            tasks = [session_db.delete(user_session)]
            if user_session.data:
                tasks.append(session_db.delete(user_session.data))

            await asyncio.gather(*tasks)
            await session_db.commit()
        except (err.MySQLError, SQLAlchemyError) as e:
            await session_db.rollback()
            logger.error(f"Database error: {e}")
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            await self._session_db_manager.close_session()
            