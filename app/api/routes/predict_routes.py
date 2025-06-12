
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.predict import IrisInput
from app.db.database import get_db
from app.db.models import Prediction
from app.utils.model_loader import session
import numpy as np

router = APIRouter(tags=["Prediction"])

label_map = {0: "Setosa", 1: "Versicolor", 2: "Virginica"}

@router.post("/", summary="Make a prediction with the Iris ONNX model")
def predict(input: IrisInput, db: Session = Depends(get_db)):
    try:
        data = np.array([input.features], dtype=np.float32)
        data = np.ascontiguousarray(data)

        if data.shape != (1, 4):
            raise HTTPException(status_code=400, detail="Input must have exactly 4 decimal values.")

        model_input = {session.get_inputs()[0].name: data}
        output = session.run(None, model_input)

        pred_class = int(np.argmax(output[0], axis=1)[0])
        pred_label = label_map.get(pred_class, "Unknown")

        prediction = Prediction(
            sepal_length=data[0][0],
            sepal_width=data[0][1],
            petal_length=data[0][2],
            petal_width=data[0][3],
            predicted_class=pred_class,
            predicted_label=pred_label
        )
        db.add(prediction)
        db.commit()
        db.refresh(prediction)

        return {
            "id": prediction.id,
            "predicted_class": pred_class,
            "predicted_label": pred_label
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
