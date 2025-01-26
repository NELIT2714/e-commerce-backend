import datetime

from fastapi import HTTPException

from project import logger
from project.database import async_session
from project.database.mariadb.models.users import Sessions, Users

from pymysql import err
from sqlalchemy.exc import SQLAlchemyError


async def create_session(session_db, user: Users, data: dict, token: str):
    session = Sessions(
        user_id=user.user_id,
        os=data["metadata"]["os"],
        browser=data["metadata"]["browser"],
        device=data["metadata"]["device"],
        ip=data["metadata"]["ip"],
        token=token,
        created_at=datetime.datetime.now()
    )
    session_db.add(session)
    await session_db.commit()
    