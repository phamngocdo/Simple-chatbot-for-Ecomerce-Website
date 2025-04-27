from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ReviewBase(BaseModel):
    product_id: int
    buyer_id: int
    rating: int
    comment: Optional[str] = None

class Review(ReviewBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
