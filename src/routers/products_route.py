from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from services.products_service import ProductService
from config.db_config import get_mysql_db as get_db

products_router = APIRouter()

@products_router.get("/")
async def get_all_products(db: Session = Depends(get_db)):
    try:
        products = await ProductService.get_all_products(db=db)
        if not products:
            raise HTTPException(status_code=404, detail="No products found")
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
    

@products_router.get("/{product_id}")
async def get_product(product_id: int, db: Session = Depends(get_db)):
    if product_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid product_id, must be greater than 0")
    try:
        product = await ProductService.get_product_by_id(db=db, product_id=product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        return product
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")