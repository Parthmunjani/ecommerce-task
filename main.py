from fastapi import FastAPI
from app.views.product import router as product_router
from app.views.user import router as user_router
from app.views.order import router as order_router

app = FastAPI()

# app.include_router(user_router, tags=["users"], prefix="/users")
app.include_router(product_router, tags=["products"], prefix="/products")
app.include_router(user_router, tags=["users"], prefix="/users")
app.include_router(order_router,tags=["order"],prefix="/user")
    