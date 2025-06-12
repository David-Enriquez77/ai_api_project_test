from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.predict import IrisInput
from app.db.database import get_db
from app.db.models import Prediction

from app.utils.model_loader import session  # <-- importamos la sesión

router = APIRouter()

label_map = {0: "Setosa", 1: "Versicolor", 2: "Virginica"}

@router.post("/predict")
def predict(input: IrisInput, db: Session = Depends(get_db)):
    data = [input.features]

    try:
        inputs = {session.get_inputs()[0].name: data}
        outputs = session.run(None, inputs)
        pred_class = int(outputs[0][0])
        pred_label = label_map.get(pred_class, "Unknown")

        # Guardar en base de datos
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
