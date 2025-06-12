from pydantic import BaseModel, Field
from typing import List

class IrisInput(BaseModel):
    features: List[float] = Field(..., min_items=4, max_items=4)
