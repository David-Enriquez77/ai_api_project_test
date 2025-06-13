from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.predict import IrisInput
from app.db.database import get_db
from app.db.models import Prediction, User
from app.utils.model_loader import session
import numpy as np
from app.auth.deps import get_current_user

router = APIRouter(tags=["Prediction"])

label_map = {0: "Setosa", 1: "Versicolor", 2: "Virginica"}

@router.post("/", summary="Make a prediction with the Iris ONNX model")
def predict(
    input: IrisInput,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Convert input features to NumPy array with required shape and type
    data = np.array([input.features], dtype=np.float32)
    data = np.ascontiguousarray(data)

    # Validate input shape (1 sample, 4 features)
    if data.shape != (1, 4):
        raise HTTPException(status_code=400, detail="Input must have exactly 4 decimal values.")

    try:
        # Prepare input for ONNX model and run inference
        model_input = {session.get_inputs()[0].name: data}
        output = session.run(None, model_input)

        # Get predicted class index and label
        pred_class = int(np.argmax(output[0], axis=1)[0])
        pred_label = label_map.get(pred_class, "Unknown")

        # Save prediction data to the database linked to current user
        prediction = Prediction(
            sepal_length=data[0][0],
            sepal_width=data[0][1],
            petal_length=data[0][2],
            petal_width=data[0][3],
            predicted_class=pred_class,
            predicted_label=pred_label,
            user_id=current_user.id,
        )
        db.add(prediction)
        db.commit()
        db.refresh(prediction)

        # Return prediction summary
        return {
            "id": prediction.id,
            "predicted_class": pred_class,
            "predicted_label": pred_label,
        }

    except Exception as e:
        # Handle errors during inference or DB operations
        raise HTTPException(status_code=500, detail=str(e))
