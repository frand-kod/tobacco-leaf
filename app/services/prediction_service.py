from fastapi import UploadFile,HTTPException
from sqlalchemy.orm import Session
from app.repository.predict_repository import PredictRepository
from app.ml.predictor import predict_from_bytes
from app.models.prediction_report import PredictionReport
from app.schemas.prediction import ReportResponse
from app.utils.resizer_image import save_resized_image
from app.utils.builder_url import build_img_url

class PredictionService:
    @staticmethod
    async def predict_and_save(db: Session, user_id: int, file: UploadFile):
        contents = await file.read()

        result = predict_from_bytes(contents)
        image_path = save_resized_image(contents)

        report = PredictionReport(
            user_id=user_id,
            image_path=image_path,
            label=result["label"],
            confidence=result["confidence"]
        )

        saved = PredictRepository.create_predict(db, report)

        return ReportResponse(
            id=saved.id,
            label=saved.label,
            image_path=build_img_url(saved.image_path),
            confidence=saved.confidence,
            created_at=saved.created_at
        )

    @staticmethod
    def get_reports(db: Session, user_id: int):
        reports = PredictRepository.get__predict_by_user(db, user_id)

        return [
            ReportResponse(
                id=r.id,
                label=r.label,
                image_path=build_img_url(r.image_path),
                confidence=r.confidence,
                created_at=r.created_at
            )
            for r in reports
        ]
        

    @staticmethod
    def get_prediction_detail(db: Session, predict_id: int, user_id: int):
        predict = PredictRepository.get_predict_by_id(db, predict_id)

        if not predict or predict.user_id != user_id:
            raise HTTPException(status_code=404, detail="Prediction not found")

        return ReportResponse(
                id=predict.id,
                label=predict.label,
                image_path=build_img_url(predict.image_path),
                confidence=predict.confidence,
                created_at=predict.created_at
            )


    @staticmethod
    def delete_predict(db: Session, predict_id: int, user_id: int):
        predict = PredictRepository.get_predict_by_id(db, predict_id)

        if not predict or predict.user_id != user_id:
            raise HTTPException(status_code=404, detail="Prediction not found")

        PredictRepository.delete_predict(db, predict)
        return {"message": "Prediction deleted"}