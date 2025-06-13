from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
# This code defines Pydantic models for input and output schemas related to Iris flower predictions.
class IrisInput(BaseModel):
    features: List[float] = Field(..., min_items=4, max_items=4)
#This model represents the input data for making predictions, requiring exactly 4 decimal values representing the features of the Iris flower. 
class PredictionOut(BaseModel):
    id: int
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float
    predicted_class: int
    predicted_label: str
    created_at: datetime

    class Config:
        orm_mode = True