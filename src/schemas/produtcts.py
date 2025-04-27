from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int
    image_urls: Optional[str] = None
    category_id: Optional[int] = None

class Product(ProductBase):
    id: int
    seller_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
