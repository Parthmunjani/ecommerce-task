
from fastapi import HTTPException
from models.users import UserModel
from database import SessionLocal
from main import app


@app.post("/users/", response_model=UserModel)
async def create_user(user_data: UserModel):
    try:
        async with SessionLocal() as db:
            query = UserModel.__table__.insert().values(**user_data.dict())
            last_record_id = await db.execute(query)
            return {**user_data.dict(), "id": last_record_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error creating user")
