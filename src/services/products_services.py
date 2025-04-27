from sqlalchemy.orm import Session
from models.products_model import ProductModel
from models.users_model import UserModel
from fastapi import HTTPException
from utils.logger import log_error

class ProductService():
    @staticmethod
    async def get_product_by_id(db: Session, product_id: int):
        if product_id <= 0:
            raise HTTPException(status_code=400, detail="Invalid product_id, must be greater than 0")
        try:
            product = db.query(ProductModel).filter(ProductModel.id == product_id).join(ProductModel.category).join(ProductModel.seller).first()
            
            if not product:
                raise HTTPException(status_code=404, detail="Product not found")
            
            return {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": product.price,
                "stock": product.stock,
                "category": product.category.name,
                "seller": product.seller.username,
                "created_at": product.created_at,
                "updated_at": product.updated_at
            }
        except Exception as e:
            log_error(f"Error fetching product by ID: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
    
    @staticmethod
    async def  get_all_products(db: Session):
        try:
            products = db.query(ProductModel).join(ProductModel.category).join(ProductModel.seller).all()
            if not products:
                raise HTTPException(status_code=404, detail="No products found")
            
            return [
                {
                    "id": product.id,
                    "name": product.name,
                    "description": product.description,
                    "price": product.price,
                    "stock": product.stock,
                    "category": product.category.name,
                    "seller": product.seller.username,
                    "created_at": product.created_at,
                    "updated_at": product.updated_at
                } for product in products
            ]
        except Exception as e:
            log_error(f"Error fetching all products: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
