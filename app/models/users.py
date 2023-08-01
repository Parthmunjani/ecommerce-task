# models.py

from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

Base = declarative_base()

class UserModel(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(50),index=True, nullable=False)
    email = Column(String(100),index=True, nullable=False)
    password = Column(String(25), nullable=False)
    phone_number = Column(String(20))
    wallet = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    modified_at = Column(DateTime, default=datetime.utcnow)

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

class OrderModel(Base):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    product_id = Column(Integer, ForeignKey('product.id'))
    quantity = Column(Integer, default=1)
    total_price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    modified_at = Column(DateTime, default=datetime.utcnow)

    user = relationship('UserModel', backref='orders')
    product = relationship('ProductModel', backref='orders')

    def __init__(self, user_id, product_id, quantity, total_price):
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity
        self.total_price = total_price

    def update_total_price(self, new_price):
        self.total_price = new_price
        self.modified_at = datetime.utcnow()
