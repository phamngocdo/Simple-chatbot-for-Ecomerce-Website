from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from services.users_service import UserService
from schemas.user_schemas import UserUpdate

from config.db_config import get_mysql_db as get_db

users_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@users_router.get("/me")
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        user = await UserService.get_current_user(token=token, db=db)
        if not user:
            raise HTTPException(status_code=401, detail="Unauthorized")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
    


@users_router.put("/me")
async def update_password(data: UserUpdate, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        user_data = {
            "password": UserUpdate.password
        }
        return await UserService.update_current_user(token=token, user_data=user_data, db=db)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")