from pydantic import BaseModel, constr


class UpdateManufacturer(BaseModel):
    name: constr(min_length=2, max_length=30) = None
