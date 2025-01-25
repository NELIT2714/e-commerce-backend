from typing import Optional
from typing_extensions import Annotated

from pydantic import BaseModel, constr, StringConstraints


class MultiLangField(BaseModel):
    en: Annotated[str, StringConstraints(min_length=2, max_length=30)]
    pl: Annotated[str, StringConstraints(min_length=2, max_length=30)]
    ru: Annotated[str, StringConstraints(min_length=2, max_length=30)]
    ua: Annotated[str, StringConstraints(min_length=2, max_length=30)]


class NewCategory(BaseModel):
    category_name: MultiLangField
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "category_name": {
                        "en": "Catergory name",
                        "pl": "Nazwa kategorii",
                        "ru": "Название категории",
                        "ua": "Назва категорії"
                    }
                }
            ]
        }
    }
