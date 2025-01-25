from typing import Optional, Literal

from pydantic import BaseModel, model_validator, Field, field_validator


class Discount(BaseModel):
    regular: Optional[int] = Field(None, description="Discount percentage for regular users")
    specialist: Optional[int] = Field(None, description="Discount percentage for specialists")


class Price(BaseModel):
    regular: float = Field(..., description="Price for regular users")
    specialist: float = Field(..., description="Price for specialists")
    discount: Optional[Discount] = None


class MultiLangField(BaseModel):
    de: Optional[str] = Field(None, description="Description in German")
    bg: Optional[str] = Field(None, description="Description in Bulgarian")


class Description(BaseModel):
    short: Optional[MultiLangField] = Field(None, description="Short description")
    detail: Optional[MultiLangField] = Field(None, description="Detail description")
    usage: Optional[MultiLangField] = Field(None, description="Product usage description")
    ingredients: Optional[MultiLangField] = Field(None, description="Ingredients description")


class NewProduct(BaseModel):
    name: str
    article: str
    category_id: int
    manufacturer_id: int
    description: Description
    price: Price
