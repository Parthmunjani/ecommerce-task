from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app.schema.product import ProductResponse
from database import get_db
from app.models.users import ProductModel

router = APIRouter()


@router.get("/", response_model=List[ProductResponse])
def get_all_products(db: Session = Depends(get_db)):
    try:
        products = db.query(ProductModel).all()
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    try:
        product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
        if product is None:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/", response_model=ProductResponse)  # Use the ProductResponse schema to return the created product
def create_product(product_data: ProductResponse, db: Session = Depends(get_db)):
    try:
        # Create a new Product model instance from the received data
        product_model = ProductModel(**product_data.dict())
        db.add(product_model)
        db.commit()
        db.refresh(product_model)  # To populate the generated fields like id
        return product_model
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))