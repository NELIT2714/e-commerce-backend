import asyncio
import bcrypt

from typing import TYPE_CHECKING, Optional, Union
from abc import ABC, abstractmethod
from pymysql import err 

from fastapi import HTTPException

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from project import logger
from project.database.mariadb.models.users import Sessions
from project.schemas.user import UserOut
from project.utils import SessionDBManager
from project.database.mariadb.models import Users, DeliveryData, PersonalData



class IUsersRepository(ABC):
    @abstractmethod
    async def get_user(self, user_id: int = None, username: str = None, email: str = None) -> Optional[Users]:
        pass
    
    @abstractmethod
    async def create_user(self, user_data: dict) -> Union[str, HTTPException]:
        pass

    @abstractmethod
    async def update_account(self, user_id: int, account_data: dict) -> Optional[HTTPException]:
        pass

    @abstractmethod
    async def update_personal_data(self, user_id: int, personal_data: dict) -> Optional[HTTPException]:
        pass
    
    @abstractmethod
    async def update_delivery_data(self, user_id: int, delivery_data: dict) -> Optional[HTTPException]:
        pass

    @abstractmethod
    async def login(self, user_data: dict) -> Union[str, HTTPException]:
        pass

    @abstractmethod
    async def logout(self, token: str) -> Optional[HTTPException]:
        pass

    # async def delete_user(self, )


class UsersRepository(IUsersRepository):
    def __init__(self, session_db: Optional[AsyncSession] = None):
        self._session_db_manager = SessionDBManager(session_db=session_db)


    async def get_user(self, user_id: int = None, username: str = None, email: str = None) -> Union[Users, HTTPException]:
        session_db = await self._session_db_manager.get_session()
        
        try:
            query = select(Users).options(selectinload(Users.personal_data), selectinload(Users.delivery_data), selectinload(Users.sessions), selectinload(Users.sessions).selectinload(Sessions.data))

            fields = {"user_id": user_id, "username": username, "email": email}
            for k, v in fields.items():
                if v:
                    query = query.filter(getattr(Users, k) == v)
                    break

            user_query = await session_db.execute(query)
            user = user_query.scalar_one_or_none()
            if user is None:
                raise HTTPException(status_code=404, detail="User not found")

            return user
        except (err.MySQLError, SQLAlchemyError) as e:
            logger.error(f"Database error: {e}")
            raise HTTPException(status_code=500, detail="Database error")
        except Exception as e:
            logger.error(f"Error in UserRepository.get: {str(e)}")
            raise HTTPException(status_code=500, detail="An unknown error occurred")
        finally:
            await self._session_db_manager.close_session()


    async def create_user(self, user_data: dict) -> Union[str, HTTPException]:
        from project.database.crud import SessionsRepository
        
        user_available = await asyncio.gather(
            self.get_user(username=user_data["username"]),
            self.get_user(email=user_data["email"])
        )

        if user_available[0]:
            raise HTTPException(status_code=400, detail="Username already in use")
        if user_available[1]:
            raise HTTPException(status_code=400, detail="Email already in use")

        session_db = await self._session_db_manager.get_session()
        session_repository = SessionsRepository(self._session_db_manager)

        try:
            user = Users(
                username=user_data["username"],
                email=user_data["email"],
                password_hash=bcrypt.hashpw(user_data["password"].encode(), bcrypt.gensalt())
            )
            session_db.add(user)
            await session_db.flush()

            token = await session_repository.create_session(user=user, data=user_data["metadata"])

            logged_user = {"id": user.user_id, "username": user_data["username"], "email": user_data["email"]}
            logger.info(f"Created new user {logged_user}")

            return token
        except (err.MySQLError, SQLAlchemyError) as e:
            await session_db.rollback()
            logger.error(f"Database error: {e}")
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            await self._session_db_manager.close_session()


    async def update_account(self, user_id: int, account_data: dict) -> Optional[HTTPException]:
        if not (user := await self.get_user(user_id=user_id)):
            raise HTTPException(status_code=404, detail="User not found")
        
        if (user_username := account_data.get("username")):
            result = await self.get_user(username=user_username)
            if result:
                raise HTTPException(status_code=400, detail="Username already in use")
            
        if (user_email := account_data.get("email")):
            result = await self.get_user(email=user_email)
            if result:
                raise HTTPException(status_code=400, detail="Email already in use")

        session_db = await self._session_db_manager.get_session()
        try:
            fields_to_update = ["username", "email"]
            for field in fields_to_update:
                if field in account_data:
                    setattr(user, field, account_data[field])
                    continue
                
            if (account_password := account_data.get("password", False)):
                if not bcrypt.checkpw(account_password["old"].encode(), user.password_hash):
                    raise HTTPException(status_code=401, detail="Incorrect old password")
                setattr(user, "password_hash", bcrypt.hashpw(account_password["new"].encode(), bcrypt.gensalt()))
            
            session_db.add(user)
            await session_db.commit()
        except (err.MySQLError, SQLAlchemyError) as e:
            await session_db.rollback()
            logger.error(f"Database error: {e}")
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            await self._session_db_manager.close_session()


    async def update_personal_data(self, user_id: int, personal_data: dict) -> Optional[HTTPException]:
        if not (user := await self.get_user(user_id=user_id)):
            raise HTTPException(status_code=404, detail="User not found")
        
        session_db = await self._session_db_manager.get_session()

        try:
            if not (user_personal_data := user.personal_data):
                session_db.add(PersonalData(user_id=user.user_id, **personal_data))
                await session_db.commit()
                return
                
            fields_to_update = ["first_name", "last_name", "phone_number"]
            for field in fields_to_update:
                if field in personal_data:
                    setattr(user_personal_data, field, personal_data[field])

            session_db.add(user_personal_data)
            await session_db.commit()
        except (err.MySQLError, SQLAlchemyError) as e:
            await session_db.rollback()
            logger.error(f"Database error: {e}")
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            await self._session_db_manager.close_session()


    async def update_delivery_data(self, user_id: int, delivery_data: dict) -> Optional[HTTPException]:
        if not (user := await self.get_user(user_id=user_id)):
            raise HTTPException(status_code=404, detail="User not found")
        
        session_db = await self._session_db_manager.get_session()

        try:
            if not (user_delivery_data := user.delivery_data):
                session_db.add(DeliveryData(user_id=user.user_id, **delivery_data))
                await session_db.commit()
                return

            fields_to_update = ["country", "city", "postcode", "address"]
            for field in fields_to_update:
                if field in delivery_data:
                    setattr(user_delivery_data, field, delivery_data[field])

            session_db.add(user_delivery_data)
            await session_db.commit()
        except (err.MySQLError, SQLAlchemyError) as e:
            await session_db.rollback()
            logger.error(f"Database error: {e}")
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            await self._session_db_manager.close_session()


    async def login(self, user_data: dict) -> Union[str, HTTPException]:
        from project.database.crud import SessionsRepository

        if not (user := await self.get_user(username=user_data["username"])):
            raise HTTPException(status_code=404, detail="User not found")
        
        if not bcrypt.checkpw(user_data["password"].encode(), user.password_hash):
            raise HTTPException(status_code=401, detail="Incorrect password")
        
        session_db = await self._session_db_manager.get_session()
        session_repository = SessionsRepository(SessionDBManager(session_db=session_db))

        try:
            token = await session_repository.create_session(user=user, data=user_data["metadata"])
            return token
        except (err.MySQLError, SQLAlchemyError) as e:
            await session_db.rollback()
            logger.error(f"Database error: {e}")
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            await self._session_db_manager.close_session()

    async def logout(self, token: str) -> Optional[HTTPException]:
        from project.database.crud import SessionsRepository
        
        session_db = await self._session_db_manager.get_session()
        session_repository = SessionsRepository(SessionDBManager(session_db=session_db))
        return await session_repository.delete_session(token=token)