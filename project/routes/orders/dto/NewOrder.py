from pydantic import BaseModel, constr


class NewManufacturer(BaseModel):
    name: constr(min_length=2, max_length=30)
