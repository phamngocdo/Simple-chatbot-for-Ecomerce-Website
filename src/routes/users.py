from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from services.users import UserService

from config.db_config import get_mysql_db as get_db

users_router = APIRouter()

@users_router.get("/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    if user_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid user_id, must be greater than 0")
    
    user = await UserService.get_user_by_id(db=db, user_id=user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")    
    
    return user

@users_router.put("/{user_id}")
async def update_user(user_id: int, user_data: dict, db: Session = Depends(get_db)):
    if user_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid user_id, must be greater than 0")

    user = await UserService.update_user(db=db, user_id=user_id, user_data=user_data)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user