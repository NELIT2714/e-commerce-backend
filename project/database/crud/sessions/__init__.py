import datetime

from fastapi import HTTPException
from sqlalchemy import select

from project import logger
from project.database import async_session
from project.database.mariadb.models.users import Sessions, Users
from project.utils import TokenService


async def create_session(session_db, user: Users, metadata: dict):
    print(metadata)
    
    token_service = TokenService()
    token = await token_service.generate_token(user_id=user.user_id)

    session = Sessions(
        user_id=user.user_id,
        os=metadata["os"],
        browser=metadata["browser"],
        device=metadata["device"],
        ip=metadata["ip"],
        token=token,
        created_at=datetime.datetime.now()
    )
    session_db.add(session)
    await session_db.commit()

    return token
    

async def delete_session(session_db, token: str):
    session_query = await session_db.execute(select(Sessions).filter_by(token=token))
    session = session_query.scalar_one_or_none()
    session_db.delete(session)
    await session_db.commit()