import bcrypt
import datetime

from fastapi import HTTPException
from pymysql import err
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload

from project import logger
from project.database import async_session
from project.database.mariadb.models import Users, Sessions

from project.utils import TokenService


async def get_user_dict(user_object):
    return {
        "id": user_object.user_id,
        "username": user_object.username,
        "email": user_object.email,
        "personal_data": {
            "first_name": user_object.personal_data.first_name,
            "last_name": user_object.personal_data.last_name,
            "phone_number": user_object.personal_data.phone_number
        },
        "delivery_data": {
            "country": user_object.delivery_data.country,
            "city": user_object.delivery_data.city,
            "postcode": user_object.delivery_data.postcode,
            "address": user_object.delivery_data.address
        }
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
        await session_db.rollback()
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

            if user_id:
                query = query.filter_by(user_id=user_id)
            if username:
                query = query.filter_by(username=username)
            if email:
                query = query.filter_by(email=email)

            user_result = await session_db.execute(query)
            user = user_result.scalar_one_or_none()

            if user is None and dump:
                raise HTTPException(status_code=404, detail="User not found")

            return await get_user_dict(user) if dump else user
    except (err.MySQLError, SQLAlchemyError) as e:
        logger.error(f"Database error: {e}")
        await session_db.rollback()
        raise HTTPException(status_code=500, detail="Database error")


async def sign_up(user_data: dict):
    try:
        async with async_session() as session_db:
            if await get_user(email=user_data["email"]):
                raise HTTPException(status_code=400, detail="Email already in use")

            user = Users(
                username=user_data["username"],
                email=user_data["email"],
                password_hash=bcrypt.hashpw(user_data["password"].encode(), bcrypt.gensalt())
            )

            session_db.add(user)
            await session_db.flush()

            token_service = TokenService()
            token = await token_service.generate_token(user_id=user.user_id, username=user.username)
            
            session = Sessions(
                user_id=user.user_id,
                os=user_data["metadata"]["os"],
                browser=user_data["metadata"]["browser"],
                device=user_data["metadata"]["device"],
                ip=user_data["metadata"]["ip"],
                token=token,
                created_at=datetime.datetime.now()
            )
            session_db.add(session)
            await session_db.commit()

            return token
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
