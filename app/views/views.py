from app.schema.user import UserCreate
from fastapi import HTTPException,Depends
from models.users import UserModel
from database import SessionLocal
from main import app,get_db
from sqlalchemy.orm import Session


@app.post("/users/")
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    try:
        # Create a new User model instance from the received data
        user_model = UserModel(**user_data.dict())
        db.add(user_model)
        db.commit()
        db.refresh(user_model)  # To populate the generated fields like id
        # Return the created user
        return user_model

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
