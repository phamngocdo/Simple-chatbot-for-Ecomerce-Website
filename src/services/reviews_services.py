from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.reviews_model import ReviewModel

class ReviewService():
    @staticmethod
    async def get_review_by_id(db: Session, review_id: int):
        if review_id <= 0:
            raise HTTPException(status_code=400, detail="Invalid review_id, must be greater than 0")
        try:
            review = db.query(ReviewModel).filter(ReviewModel.id == review_id).first()
            if not review:
                raise HTTPException(status_code=404, detail="Review not found")
            return review
        except Exception as e:
            raise HTTPException(status_code=500, detail="Internal server error")
    
    @staticmethod
    async def get_review_by_product_id(db: Session, product_id: int):
        if product_id <= 0:
            raise HTTPException(status_code=400, detail="Invalid product_id, must be greater than 0")
        try:
            reviews = db.query(ReviewModel).filter(ReviewModel.product_id == product_id).all()
            if not reviews:
                raise HTTPException(status_code=404, detail="Product does not have review yet")
            return reviews
        except Exception as e:
            raise HTTPException(status_code=500, detail="Internal server error")