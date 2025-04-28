from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.db_config import get_mysql_db as get_db
from services.reviews_services import ReviewService

reviews_router = APIRouter()

@reviews_router.get("/{review_id}")
async def get_review(review_id:int, db: Session = Depends(get_db)):
    return await ReviewService.get_review_by_id(db=db, review_id=review_id)

@reviews_router.get("/product/{product_id}")
async def get_review_by_product(product_id: int, db: Session = Depends(get_db)):
    return await ReviewService.get_review_by_product_id(db=db, product_id=product_id)