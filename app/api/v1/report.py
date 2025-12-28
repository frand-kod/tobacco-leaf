from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.api.deps import get_current_user,get_database
from app.services.prediction_service import PredictionService
from app.schemas.prediction import ReportResponse

from app.models.user import User

router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
    dependencies = [Depends(get_current_user)]
)

@router.get("/", response_model=List[ReportResponse])
def my_reports(
    db: Session = Depends(get_database),
    current_user: User = Depends(get_current_user)
):
    return PredictionService.get_reports(
        db=db,
        user_id=current_user.id
    )


@router.get("/{predict_id}", response_model=ReportResponse)
def report_detail(
    predict_id: int,
    db: Session = Depends(get_database),
    current_user: User = Depends(get_current_user)
):
    return PredictionService.get_prediction_detail(
        db=db,
        predict_id=predict_id,
        user_id=current_user.id
    )

@router.delete("/{predict_id}")
def delete_report(
    predict_id: int,
    db: Session = Depends(get_database),
    current_user: User = Depends(get_current_user)
):
    return PredictionService.delete_predict(
        db=db,
        predict_id=predict_id,
        user_id=current_user.id
    )