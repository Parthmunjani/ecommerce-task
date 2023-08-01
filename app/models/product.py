# models/product.py

from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class ProductModel(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    modified_at = Column(DateTime, default=datetime.utcnow)

    def purchase_product(self, user):
        discount_amount = self.price * 0.1
        user.wallet += discount_amount
        user.modified_at = datetime.utcnow()
        return discount_amount
