from typing import List
from pydantic import BaseModel, Field, validator


class CardBaseSchema(BaseModel):
    nm_id: int | None
    name: str
    brand: str
    brand_id: int
    site_brand_id: int
    supplier_id: int
    sale: int
    price: int
    sale_price: int
    rating: int
    feedbacks: int

    class Config:
        orm_mode = True


class CardParseSchema(CardBaseSchema):
    nm_id: int | None = Field(alias="id")
    brand_id: int = Field(alias="brandId")
    site_brand_id: int = Field(alias="siteBrandId")
    supplier_id: int = Field(alias="supplierId")
    price: int = Field(alias="priceU")
    sale_price: int = Field(alias="salePriceU")

    @validator('price', 'sale_price')
    def remove_zeroes(cls, value):
        return value // 100

    class Config:
        orm_mode = True


class ColorBaseSchema(BaseModel):
    name: str
    id: int

    class Config:
        orm_mode = True


class CardSchema(CardBaseSchema):
    colors: List[ColorBaseSchema]
