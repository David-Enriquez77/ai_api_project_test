from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from app.db.database import get_db
from app.db.models import Prediction, User
from app.schemas.predict import PredictionOut
from app.auth.deps import get_current_user

router = APIRouter(tags=["Prediction History"])

@router.get("/", response_model=List[PredictionOut], summary="Get prediction history for the current user")
def get_predictions(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    predictions = (
        db.query(Prediction)
        .filter(Prediction.user_id == current_user.id)
        .order_by(Prediction.created_at.desc())
        .all()
    )
    return predictions

@router.get("/{prediction_id}", response_model=PredictionOut, summary="Get detailed info of a prediction by ID")
def get_prediction_detail(
    prediction_id: int = Path(..., description="The ID of the prediction to retrieve"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    prediction = db.query(Prediction).filter(Prediction.id == prediction_id).first()

    if not prediction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prediction not found")

    if prediction.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this prediction")

    return prediction

