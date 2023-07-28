from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from models.users import Base

class ProductModel(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    modified_at = Column(DateTime, default=datetime.utcnow)

    def purchase_product(self, user):
        discount_amount = self.price * 0.1 # Calculate 10% of the product price
        # Update the user's wallet by adding the discount_amount
        user.wallet += discount_amount
        # Optionally, you can update the modified_at timestamp of the user
        user.modified_at = datetime.utcnow()
        # Return the discount amount for any further processing or displaying to the user
        return discount_amount
