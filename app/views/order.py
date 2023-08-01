from fastapi import HTTPException,APIRouter,Depends
from app.schema.order import OrderRequest
from app.models.users import UserModel
from app.models.users import ProductModel
from app.models.users import OrderModel
from database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/{order_id}", response_model=OrderRequest)
def get_order(order_id: int, db: Session = Depends(get_db)):
    try:
        order = db.query(OrderModel).filter(OrderModel.id == order_id).first()
        if order is None:
            raise HTTPException(status_code=404, detail="Order not found")
        return order
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/orders/", response_model=OrderRequest)
def create_order(order_data: OrderRequest, db: Session = Depends(get_db)):
    try:
        user = db.query(UserModel).filter(UserModel.id == order_data.user_id).first()
        product = db.query(ProductModel).filter(ProductModel.id == order_data.product_id).first()

        if user is None or product is None:
            raise HTTPException(status_code=404, detail="User or Product not found")

        # Calculate the total price for the order without the discount
        total_price = product.price * order_data.quantity
        # Calculate the total price with the 10% discount, capped at 1000 rupees
        discounted_total_price = min(total_price * 0.1, 1000)

        order = OrderModel(
            user_id=order_data.user_id,
            product_id=order_data.product_id,
            quantity=order_data.quantity,
            total_price=total_price,
        )
        db.add(order)
        db.commit()
        db.refresh(order)

        if user.wallet is None:
            user.wallet = 0

        # Calculate the amount to deduct from the wallet (50% of wallet balance or discounted_total_price, whichever is smaller)
        wallet_deduction = min(user.wallet * 0.5, total_price)

        user.wallet -= wallet_deduction
        db.commit()
       
        wallet_increase = min(total_price * 0.1, 1000)#ad in wallet
        user.wallet += wallet_increase
        db.commit()
        return order
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
