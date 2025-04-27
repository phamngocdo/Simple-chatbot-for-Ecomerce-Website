from sqlalchemy.orm import Session
from models.users import UserModel
class UserService():
    @staticmethod
    async def get_user_by_id(db: Session, user_id: int):
        return db.query(UserModel).filter(UserModel.id == user_id).first()
    
    @staticmethod
    async def create_user(db: Session, user_data: dict):
        new_user = UserModel(**user_data)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    
    @staticmethod
    async def update_user(db: Session, user_id: int, user_data: dict):
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            return None
        for key, value in user_data.items():
            setattr(user, key, value)
        db.commit()
        db.refresh(user)
        return user