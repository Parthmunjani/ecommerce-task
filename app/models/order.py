# models/order.py

from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from app.models.product import ProductModel
from app.models.users import UserModel

Base = declarative_base()

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
