from typing import Optional
from typing_extensions import Annotated

from pydantic import BaseModel, StringConstraints


class MultiLangField(BaseModel):
    en: Optional[Annotated[str, StringConstraints(min_length=2, max_length=30)]] = None
    pl: Optional[Annotated[str, StringConstraints(min_length=2, max_length=30)]] = None
    ru: Optional[Annotated[str, StringConstraints(min_length=2, max_length=30)]] = None
    ua: Optional[Annotated[str, StringConstraints(min_length=2, max_length=30)]] = None


class UpdateCategory(BaseModel):
    category_name: MultiLangField

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "category_name": {
                        "en": "New catergory name",
                        "pl": "Nowa nazwa kategorii ",
                        "ru": "Новое название категории",
                        "ua": "Нова назва категорії"
                    }
                }
            ]
        }
    }
