from pydantic import BaseModel, constr


class MultiLangField(BaseModel):
    de: constr(min_length=2, max_length=30)
    bg: constr(min_length=2, max_length=30)


class NewCategory(BaseModel):
    category_name: MultiLangField
