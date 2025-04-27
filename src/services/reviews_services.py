from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.reviews_model import ReviewModel
from utils.logger import log_error

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
            log_error(f"Error fetching review by ID: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
