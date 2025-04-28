from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from services.products_services import ProductService
from config.db_config import get_mysql_db as get_db

products_router = APIRouter()

@products_router.get("/")
async def get_all_products(db: Session = Depends(get_db)):
    return await ProductService.get_all_products(db=db)

@products_router.get("/{product_id}")
async def get_product(product_id: int, db: Session = Depends(get_db)):
    return await ProductService.get_product_by_id(db=db, product_id=product_id)