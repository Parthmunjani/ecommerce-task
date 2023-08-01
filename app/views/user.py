from app.schema.user import UserCreate
from fastapi import HTTPException,Depends,APIRouter
from app.models.users import UserModel
from database import get_db
from sqlalchemy.orm import Session
from app.schema.user import UserCreate,UserResponse
from typing import List

router = APIRouter()


@router.get("/", response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    try:
        users = db.query(UserModel).all()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    try:
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/")
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
