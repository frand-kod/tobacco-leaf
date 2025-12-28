# app/api/v1/prediction.py
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.schemas.prediction import PredictionResponse,ReportResponse

from typing import List
from app.models.user import User
from app.db.session import SessionLocal
from app.services.prediction_service import PredictionService
from app.api.deps import get_current_user,get_database

router = APIRouter(
    prefix="/model",
    tags=["Prediction"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/predict", response_model=ReportResponse)
async def predict_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_database),
    current_user: User = Depends(get_current_user)
):
    return await PredictionService.predict_and_save(
        db=db,
        user_id=current_user.id,
        file=file
    )
# fix other hands

