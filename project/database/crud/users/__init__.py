import asyncio
import bcrypt

from fastapi import HTTPException
from pymysql import err
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload

from project import logger
from project.database import async_session
from project.database.crud.sessions import create_session, delete_session
from project.database.mariadb.models import Users

from project.database.mariadb.models.users import DeliveryData, PersonalData, Sessions
from project.utils import TokenService


async def get_user_dict(user_object):
    personal_data = user_object.personal_data
    delivery_data = user_object.delivery_data

    return {
        "id": user_object.user_id,
        "username": user_object.username,
        "email": user_object.email,
        "personal_data": {
            "first_name": personal_data.first_name,
            "last_name": personal_data.last_name,
            "phone_number": personal_data.phone_number
        } if personal_data else None,
        "delivery_data": {
            "country": delivery_data.country,
            "city": delivery_data.city,
            "postcode": delivery_data.postcode,
            "address": delivery_data.address
        } if delivery_data else None,
    }



async def get_users(dump: bool = False):
    try:
        async with async_session() as session_db:
            users_query = await session_db.execute(select(Users).options(
                selectinload(Users.personal_data),
                selectinload(Users.delivery_data),
            ))
            users = users_query.scalars().all()

            return [await get_user_dict(user) for user in users] if dump else users
    except (err.MySQLError, SQLAlchemyError) as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database error")


async def get_user(user_id: int = None, username: str = None, email: str = None, dump: bool = False):
    if not any([user_id, username, email]):
        raise ValueError("At least one search parameter (user_id, username, email) must be provided")

    try:
        async with async_session() as session_db:
            query = select(Users).options(
                selectinload(Users.personal_data),
                selectinload(Users.delivery_data)
            )

            fields = {"user_id": user_id, "username": username, "email": email}
            for k, v in fields.items():
                if v:
                    query = query.filter(getattr(Users, k) == v)
                    break

            user_result = await session_db.execute(query)
            user = user_result.scalar_one_or_none()

            if user is None and dump:
                raise HTTPException(status_code=404, detail="User not found")

            return await get_user_dict(user) if dump else user
    except (err.MySQLError, SQLAlchemyError) as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database error")


async def sign_up(user_data: dict):
    try:
        async with async_session() as session_db:
            user_available = await asyncio.gather(
                get_user(username=user_data["username"]),
                get_user(email=user_data["email"])
            )

            if user_available[0]:
                raise HTTPException(status_code=400, detail="Username already in use")
            
            if user_available[1]:
                raise HTTPException(status_code=400, detail="Email already in use")

            user = Users(
                username=user_data["username"],
                email=user_data["email"],
                password_hash=bcrypt.hashpw(user_data["password"].encode(), bcrypt.gensalt())
            )

            session_db.add(user)
            await session_db.flush()

            token = await create_session(session_db=session_db, user=user, metadata=user_data["metadata"])

            logged_user = {"id": user.user_id, "username": user_data["username"], "email": user_data["email"]}
            logger.info(f"Created new user {logged_user}")

            return token
    except (err.MySQLError, SQLAlchemyError) as e:
        logger.error(f"Database error: {e}")
        await session_db.rollback()
        raise HTTPException(status_code=500, detail="Database error")


async def sign_in(user_data: dict):
    try:
        async with async_session() as session_db:
            if not (user := await get_user(username=user_data["username"])):
                raise HTTPException(status_code=404, detail="User not found")

            if not bcrypt.checkpw(user_data["password"].encode(), user.password_hash):
                raise HTTPException(status_code=401, detail="Incorrect password")
        
            token = await create_session(session_db=session_db, user=user, metadata=user_data["metadata"])
            return token
    except (err.MySQLError, SQLAlchemyError) as e:
        logger.error(f"Database error: {e}")
        await session_db.rollback()
        raise HTTPException(status_code=500, detail="Database error")


async def update_account(user_id: int, account_data: dict):
    try:
        async with async_session() as session_db:
            if not (user := await get_user(user_id=user_id)):
                raise HTTPException(status_code=404, detail="User not found")

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
        logger.error(f"Database error: {e}")
        await session_db.rollback()
        raise HTTPException(status_code=500, detail="Database error")


async def update_personal_data(user_id: int, personal_data: dict):
    try:
        async with async_session() as session_db:
            if not (user := await get_user(user_id=user_id)):
                raise HTTPException(status_code=404, detail="User not found")

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
        logger.error(f"Database error: {e}")
        await session_db.rollback()
        raise HTTPException(status_code=500, detail="Database error")


async def update_delivery_data(user_id: int, delivery_data: dict):
    try:
        async with async_session() as session_db:
            if not (user := await get_user(user_id=user_id)):
                raise HTTPException(status_code=404, detail="User not found")
            
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
        logger.error(f"Database error: {e}")
        await session_db.rollback()
        raise HTTPException(status_code=500, detail="Database error")


#
# async def update_category(category_id: int, category_data: dict, dump: bool = False):
#     try:
#         async with async_session() as session_db:
#             category_object = await get_category(category_id)
#             for translation in category_object.translations:
#                 if translation.language in category_data["category_name"]:
#                     translation.category_name = category_data["category_name"][translation.language]
#
#             session_db.add(category_object)
#
#             await session_db.commit()
#             await session_db.refresh(category_object)
#
#             return await get_category(category_id, dump=dump)
#     except (err.MySQLError, SQLAlchemyError) as e:
#         logger.error(f"Database error: {e}")
#         await session_db.rollback()
#         raise HTTPException(status_code=500, detail="Database error")
