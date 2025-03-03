from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional, Union

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException

from project.utils import SessionDBManager
from project.database.mariadb.models import Categories

# if TYPE_CHECKING:
#     from project.utils.session_db_manager import SessionDBManager


class ICategoriesRepository(ABC):
    # @abstractmethod
    # async def get_categories(self) -> Union[list[Categories], HTTPException]:
    #     pass

    @abstractmethod
    async def get_category(self, category_id: int) -> Union[Categories, HTTPException]:
        pass

    # @abstractmethod
    # async def create_category(self, category_data: dict) -> Optional[HTTPException]:
    #     pass

    # @abstractmethod
    # async def update_category(self, category_id: int, category_data: dict) -> Optional[HTTPException]:
    #     pass

    # @abstractmethod
    # async def delete_category(self, category_id: int) -> Union[list[Categories], HTTPException]:
    #     pass


class CategoriesRepository(ICategoriesRepository):
    def __init__(self, session_db: Optional[AsyncSession] = None):
        self._session_db_manager = SessionDBManager(session_db=session_db)

    async def get_category(self, category_id: int) -> Union[Categories, HTTPException]:
        session_db = await self._session_db_manager.get_session()

        category_query = await session_db.execute(select(Categories).options(
            selectinload(Categories.translations)
        ).filter_by(category_id=category_id))
        return category_query.scalar_one_or_none()

