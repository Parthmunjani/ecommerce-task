from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

db_host = os.environ.get('DB_HOST', 'localhost')
db_username = os.environ.get('DB_USERNAME', 'postgres')
db_password = os.environ.get('DB_PASSWORD', 'password')
db_name = os.environ.get('DB_NAME', 'mydb')

# Form the DATABASE_URL string using the environment variables
DATABASE_URL = f"postgresql://{db_username}:{db_password}@{db_host}/{db_name}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
