from models.users import UserModel
from pydantic import BaseModel
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, Depends
from app.schema.user import UserCreate
from fastapi.responses import JSONResponse  # Import JSONResponse
from typing import List
app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/", response_model=List[UserCreate])
def get_all_users(db: Session = Depends(get_db)):
    try:
        users = db.query(UserModel).all()
        return JSONResponse(content=[user.dict() for user in users], status_code=200)
    except Exception as e:
        return JSONResponse(content={"message":e}, status_code=500)
@app.get("/users/{user_id}", response_model=List[UserCreate])
def get_user(user_id: int, db: Session = Depends(get_db)):
    try:
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        return JSONResponse(content={"message": e}, status_code=500)

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
        raise HTTPException(status_code=500, detail="Error creating user")


