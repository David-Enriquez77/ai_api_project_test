from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.db import models
from app.schemas.user import UserResponse

router = APIRouter()
#retrieve all users from the database for depuration purposes
@router.get("/", response_model=List[UserResponse], tags=["Users"])
def list_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()
