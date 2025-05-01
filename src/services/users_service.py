import traceback
from sqlalchemy.orm import Session
from models.users_model import UserModel
from utils.security import decode_token

class UserService():
    @staticmethod
    async def get_user_by_id(user_id: int, db: Session):
        try:
            return db.query(UserModel).filter(UserModel.id == user_id).first()
        except Exception as e:
            traceback.print_exc()
            raise 
    
    @staticmethod
    async def get_user_by_email(email: str, db: Session):
        try:
            return db.query(UserModel).filter(UserModel.email == email).first()
        except Exception as e:
            traceback.print_exc()
            raise 
    
    @staticmethod
    async def get_current_user(token: str, db: Session):
        try:
            user_id = decode_token(token).get("sub")
            print(user_id)
            return db.query(UserModel).filter(UserModel.id == user_id).first()
        except Exception as e:
            traceback.print_exc()
            raise
    
    @staticmethod
    async def update_user(user_id: int, user_data: dict, db: Session):
        try:
            user = db.query(UserModel).filter(UserModel.id == user_id).first()
            if not user:
                return None
            for key, value in user_data.items():
                setattr(user, key, value)
            db.commit()
            db.refresh(user)
            return user
        except Exception as e:
            traceback.print_exc()
            raise