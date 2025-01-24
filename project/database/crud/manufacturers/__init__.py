from fastapi import HTTPException
from pymysql import err
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from project import logger
from project.database import async_session
from project.database.mariadb.models import Manufacturers


async def get_manufacturer_dict(manufacturer_object):
    return {
        "id": manufacturer_object.manufacturer_id,
        "name": manufacturer_object.manufacturer_name,
    }


async def get_manufacturers(dump: bool = False):
    try:
        async with async_session() as session_db:
            manufacturers_query = await session_db.execute(select(Manufacturers))
            manufacturers_objects = manufacturers_query.scalars().all()

            return [await get_manufacturer_dict(manufacturer_objects) for manufacturer_objects in
                    manufacturers_objects] if dump else manufacturers_objects
    except (err.MySQLError, SQLAlchemyError) as e:
        logger.error(f"Database error: {e}")
        await session_db.rollback()
        raise HTTPException(status_code=500, detail="Database error")


async def get_manufacturer(manufacturer_id: int, dump: bool = False):
    try:
        async with async_session() as session_db:
            manufacturer_query = await session_db.execute(select(Manufacturers).filter_by(manufacturer_id=manufacturer_id))
            manufacturer_object = manufacturer_query.scalar_one_or_none()

            if manufacturer_object is None:
                raise HTTPException(status_code=404, detail="Manufacturer not found")

            return await get_manufacturer_dict(manufacturer_object) if dump else manufacturer_object
    except (err.MySQLError, SQLAlchemyError) as e:
        logger.error(f"Database error: {e}")
        await session_db.rollback()
        raise HTTPException(status_code=500, detail="Database error")


async def create_manufacturer(manufacturer_data: dict, dump: bool = False):
    try:
        async with async_session() as session_db:
            manufacturer = Manufacturers(**manufacturer_data)
            session_db.add(manufacturer)

            await session_db.commit()

            return await get_manufacturer(manufacturer.manufacturer_id, dump=dump)
    except (err.MySQLError, SQLAlchemyError) as e:
        logger.error(f"Database error: {e}")
        await session_db.rollback()
        raise HTTPException(status_code=500, detail="Database error")


async def update_manufacturer(manufacturer_id: int, manufacturer_data: dict, dump: bool = False):
    try:
        async with async_session() as session_db:
            manufacturer_object = await get_manufacturer(manufacturer_id)
            manufacturer_object.manufacturer_name = manufacturer_data["manufacturer_name"]
            session_db.add(manufacturer_object)

            await session_db.commit()

            return await get_manufacturer(manufacturer_id, dump=dump)
    except (err.MySQLError, SQLAlchemyError) as e:
        logger.error(f"Database error: {e}")
        await session_db.rollback()
        raise HTTPException(status_code=500, detail="Database error")


async def delete_manufacturer(manufacturer_id: int, dump: bool = False):
    try:
        async with async_session() as session_db:
            manufacturer_object = await get_manufacturer(manufacturer_id)

            await session_db.delete(manufacturer_object)
            await session_db.commit()

            return await get_manufacturers(dump)
    except (err.MySQLError, SQLAlchemyError) as e:
        logger.error(f"Database error: {e}")
        await session_db.rollback()
        raise HTTPException(status_code=500, detail="Database error")
