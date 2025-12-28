# app/api/v1/prediction.py
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.schemas.prediction import PredictionResponse

from typing import List

from app.db.session import SessionLocal
from app.services.prediction_service import PredictionService
from app.api.deps import get_current_user

router = APIRouter(
    prefix="/model",
    tags=["Prediction"],
    dependencies=[Depends(get_current_user)]
)

def get_database():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/predict", response_model = PredictionResponse)
async def predict_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_database),
):
   # print("CURRENT USER:", current_user)  # 👈 DI SINI
    return await PredictionService.predict_and_save(
        db=db,
        user_id=current_user.id,
        file=file
    )
@router.get("/predict/list",response_model = List[ReportResponse])
def get_predicts(
    db : Session=Depends(get_database)
):
    return PredictionService.get_predicts(db)

@router.delete("/predict/{predict_id}")
async def delete_prediction(
    predict_id: int,
    db: Session = Depends(get_database),
):
    return await PredictionService.delete_predict(
        db=db,
        predict_id=predict_id,
        user_id=current_user.id
    )

# fix other hands

