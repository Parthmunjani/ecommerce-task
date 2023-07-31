from models.users import UserModel,ProductModel,OrderModel
from pydantic import BaseModel
from database import engine, SessionLocal,get_db
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, Depends
from app.schema.user import UserCreate,UserResponse
from fastapi.responses import JSONResponse  # Import JSONResponse
from typing import List
from app.schema.product import ProductResponse
from app.schema.order import OrderRequest

app = FastAPI()


@app.get("/users/", response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    try:
        users = db.query(UserModel).all()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    try:
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/users/")
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    try:
        # Create a new User model instance from the received data
        user_model = UserModel(**user_data.dict())
        db.add(user_model)
        db.commit()
        db.refresh(user_model)  # To populate the generated fields like id
        return user_model
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/products/", response_model=List[ProductResponse])
def get_all_products(db: Session = Depends(get_db)):
    try:
        products = db.query(ProductModel).all()
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    try:
        product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
        if product is None:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/users/orders/", response_model=OrderRequest)
def create_order(order_data: OrderRequest, db: Session = Depends(get_db)):
    try:
        # Fetch the user and product models
        user = db.query(UserModel).filter(UserModel.id == order_data.user_id).first()
        product = db.query(ProductModel).filter(ProductModel.id == order_data.product_id).first()

        if user is None or product is None:
            raise HTTPException(status_code=404, detail="User or Product not found")

        # Calculate the total price for the order without the discount
        total_price = product.price * order_data.quantity

        # Calculate the total price with the 10% discount, capped at 1000 rupees
        discounted_total_price = min(total_price * 0.1, 1000)

        # Create an order
        order = OrderModel(
            user_id=order_data.user_id,
            product_id=order_data.product_id,
            quantity=order_data.quantity,
            total_price=total_price,
        )
        db.add(order)
        db.commit()
        db.refresh(order)

        # Ensure user has a valid wallet before performing the addition
        if user.wallet is None:
            user.wallet = 0

        # Update the user's wallet with the discounted total price
        user.wallet += discounted_total_price
        db.commit()

        return order

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



