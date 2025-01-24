from fastapi import HTTPException
from pymysql import err
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload

from project import logger
from project.database import async_session
from project.database.mariadb.models import Categories, CategoriesTranslations


async def get_category_dict(category_object):
    return {
        "id": category_object.category_id,
        "name": {item.language: item.category_name for item in category_object.translations},
    }


async def get_categories(dump: bool = False):
    try:
        async with async_session() as session_db:
            categories_query = await session_db.execute(select(Categories).options(
                selectinload(Categories.translations)
            ))
            categories_objects = categories_query.scalars().all()

            return [await get_category_dict(category_object) for category_object in
                    categories_objects] if dump else categories_objects
    except (err.MySQLError, SQLAlchemyError) as e:
        logger.error(f"Database error: {e}")
        await session_db.rollback()
        raise HTTPException(status_code=500, detail="Database error")


async def get_category(category_id: int, dump: bool = False):
    try:
        async with async_session() as session_db:
            category_query = await session_db.execute(select(Categories).options(
                selectinload(Categories.translations)
            ).filter_by(category_id=category_id))
            category_object = category_query.scalar_one_or_none()

            if category_object is None:
                raise HTTPException(status_code=404, detail="Category not found")

            return await get_category_dict(category_object) if dump else category_object
    except (err.MySQLError, SQLAlchemyError) as e:
        logger.error(f"Database error: {e}")
        await session_db.rollback()
        raise HTTPException(status_code=500, detail="Database error")


async def create_category(category_data: dict, dump: bool = False):
    try:
        async with async_session() as session_db:
            category = Categories()
            session_db.add(category)

            await session_db.flush()

            for language, category_name in category_data["category_name"].items():
                translation = CategoriesTranslations(category_id=category.category_id, language=language,
                                                     category_name=category_name)
                session_db.add(translation)

            await session_db.commit()

            return await get_category(category.category_id, dump=dump)
    except (err.MySQLError, SQLAlchemyError) as e:
        logger.error(f"Database error: {e}")
        await session_db.rollback()
        raise HTTPException(status_code=500, detail="Database error")


async def update_category(category_id: int, category_data: dict, dump: bool = False):
    try:
        async with async_session() as session_db:
            category_object = await get_category(category_id)
            for translation in category_object.translations:
                if translation.language in category_data["category_name"]:
                    translation.category_name = category_data["category_name"][translation.language]

            session_db.add(category_object)

            await session_db.commit()
            await session_db.refresh(category_object)

            return await get_category(category_id, dump=dump)
    except (err.MySQLError, SQLAlchemyError) as e:
        logger.error(f"Database error: {e}")
        await session_db.rollback()
        raise HTTPException(status_code=500, detail="Database error")


async def delete_category(category_id: int, dump: bool = False):
    try:
        async with async_session() as session_db:
            category_object = await get_category(category_id)
            translations = category_object.translations

            await session_db.delete(category_object)
            for translation in translations:
                await session_db.delete(translation)

            await session_db.commit()

            return await get_categories(dump)
    except (err.MySQLError, SQLAlchemyError) as e:
        logger.error(f"Database error: {e}")
        await session_db.rollback()
        raise HTTPException(status_code=500, detail="Database error")
