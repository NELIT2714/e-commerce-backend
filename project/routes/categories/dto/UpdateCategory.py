from typing import Optional

from pydantic import BaseModel, constr


class MultiLangField(BaseModel):
    de: Optional[constr(min_length=2, max_length=30)] = None
    bg: Optional[constr(min_length=2, max_length=30)] = None


class UpdateCategory(BaseModel):
    category_name: MultiLangField
