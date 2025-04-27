from sqlalchemy import Column, Integer, String, Text, Enum, TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import relationship
from config.db_config import Base

class OrderItemsModel(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id', ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id', ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    price = Column(Integer, nullable=False)

    product = relationship("ProductModel", backref="order_items")

class OrdersModel(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    buyer_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    total_price = Column(Integer, nullable=False)
    full_name =Column(String(100), nullable=False)
    phone_number = Column(String(20), nullable=False)
    street = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    postal_code = Column(String(20), nullable=False)
    status = Column(Enum('pending', 'confirmed', 'shipped', 'completed', 'cancelled'), nullable=False, default="pending")
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)

    buyer = relationship("UserModel", backref="orders")
    order_items = relationship("OrderItemsModel", backref="order")