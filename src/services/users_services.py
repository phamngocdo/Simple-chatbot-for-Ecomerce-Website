from fastapi import HTTPException

from sqlalchemy.orm import Session
from models.users_model import UserModel
from utils.logger import log_error

class UserService():
    @staticmethod
    async def get_user_by_id(db: Session, user_id: int):
        if user_id <= 0:
            raise HTTPException(status_code=400, detail="Invalid user_id, must be greater than 0")
        try:
            user = db.query(UserModel).filter(UserModel.id == user_id).first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return user
        except Exception as e:
            log_error(f"Error fetching user by ID: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
    
    @staticmethod
    async def create_user(db: Session, user_data: dict):
        try:
            new_user = UserModel(**user_data)
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return new_user
        except Exception as e:
            log_error(f"Error creating user: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
    
    @staticmethod
    async def update_user(db: Session, user_id: int, user_data: dict):
        if user_id <= 0:
            raise HTTPException(status_code=400, detail="Invalid user_id, must be greater than 0")
        try:
            user = db.query(UserModel).filter(UserModel.id == user_id).first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            for key, value in user_data.items():
                setattr(user, key, value)
            db.commit()
            db.refresh(user)
            return user
        except Exception as e:
            log_error(f"Error updating user: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")