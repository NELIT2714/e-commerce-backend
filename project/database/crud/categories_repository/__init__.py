from abc import ABC, abstractmethod
from typing import Union

from project.database.mariadb.models import Categories


class ICategoriesRepository(ABC):
    @abstractmethod
    async def get_category(self, category_id: int):
        pass

