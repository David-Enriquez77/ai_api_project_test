
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.db.models import Prediction, User
from app.schemas.predict import PredictionOut
from app.auth.deps import get_current_user

router = APIRouter(tags=["Prediction History"])

@router.get("/", response_model=List[PredictionOut], summary="Get prediction history for the current user")
def get_predictions(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    predictions = db.query(Prediction).filter(Prediction.user_id == current_user.id).order_by(Prediction.created_at.desc()).all()
    return predictions
