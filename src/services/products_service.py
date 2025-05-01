import traceback
from sqlalchemy.orm import Session
from models.products_model import ProductModel

class ProductService():
    @staticmethod
    async def get_product_by_id(product_id: int, db: Session):
        try:
            product = db.query(ProductModel).filter(ProductModel.id == product_id).join(ProductModel.category).join(ProductModel.seller).first()
            
            if not product:
                return None
            
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
            traceback.print_exc()
            raise
    
    @staticmethod
    async def  get_all_products(db: Session):
        try:
            products = db.query(ProductModel).join(ProductModel.category).join(ProductModel.seller).all()
            if not products:
                None
            
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
            traceback.print_exc()
            raise
