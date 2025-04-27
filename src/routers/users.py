from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from services.users_services import UserService
from config.db_config import get_mysql_db as get_db

users_router = APIRouter()

@users_router.get("/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    return await UserService.get_user_by_id(db=db, user_id=user_id)

@users_router.put("/{user_id}")
async def update_user(user_id: int, user_data: dict, db: Session = Depends(get_db)):
    return await UserService.update_user(db=db, user_id=user_id, user_data=user_data)