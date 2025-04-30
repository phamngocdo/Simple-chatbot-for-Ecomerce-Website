from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session
from services.users_services import UserService
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

@users_router.get("/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    if user_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid user_id, must be greater than 0")
    try:
        user = await UserService.get_user_by_id(db=db, user_id=user_id)
        if not user:
            raise HTTPException(status_code=400, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@users_router.put("/{user_id}")
async def update_user(user_id: int, user_data: dict, db: Session = Depends(get_db)):
    if user_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid user_id, must be greater than 0")
    try:
        user = await UserService.update_user(db=db, user_id=user_id, user_data=user_data)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
