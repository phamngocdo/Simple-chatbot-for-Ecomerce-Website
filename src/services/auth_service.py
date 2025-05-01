import string
import secrets
import traceback
from sqlalchemy.orm import Session
from config.db_config import Base
from models.users_model import UserModel
from utils.security import hash_password, verify_password, create_access_token, decode_token

class AuthService:
    @staticmethod
    async def login(db: Session, user_data: dict):
        email = user_data.get("email")
        password = user_data.get("password")

        try:
            user = db.query(UserModel).filter(UserModel.email == email).first()

            if not user or not verify_password(password, user.password):
                raise ValueError("Invalid email or password")

            if not verify_password(password, user.password):
                raise ValueError("Invalid email or password")
            
            access_token = create_access_token(data={"sub": str(user.id)})
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "username": user.username
                }
            }
        except Exception as e:
            traceback.print_exc()
            raise

    @staticmethod
    async def login_with_google(db: Session, email: str):
        try:
            user = db.query(UserModel).filter(UserModel.email == email).first()
            if not user:
                characters = string.ascii_letters + string.digits
                random_pw  = ''.join(secrets.choice(characters) for i in range(20))
                username = email.split('@')[0]
                user = UserModel(username=username, email=email, password=hash_password(random_pw))
                db.add(user)
                db.commit()
                db.refresh(user)

            access_token = create_access_token(data={"sub": str(user.id)})
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "username": user.username
                }
            }
        except Exception as e:
            traceback.print_exc()
            raise

    @staticmethod
    async def register(db: Session, user_data: dict):
        email = user_data.get("email")
        username = user_data.get("username")
        phone = user_data.get("phone")
        password = user_data.get("password")
        try:
            user_email = db.query(UserModel).filter(UserModel.email == email).first()
            if user_email:
                raise ValueError("Email already exists")
            
            user_username = db.query(UserModel).filter(UserModel.username == username).first()
            if user_username:
                raise ValueError("Username already exists")
            
            hash_pw = hash_password(password)

            new_user = UserModel(
                username=username,
                email=email,
                phone=phone,
                password=hash_pw
            )

            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            
        except Exception as e:
            traceback.print_exc()
            raise 

