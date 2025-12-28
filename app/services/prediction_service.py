from fastapi import UploadFile
from sqlalchemy.orm import Session
from app.repository.predict_repository import Prediction

from app.ml.predictor import predict_from_bytes
from app.models.prediction_report import Prediction
from app.utils.resizer_image import save_resized_image

class PredictionService:
    @staticmethod
    async def predict_and_save(
        db: Session,
        user_id: int,
        file: UploadFile
    ):
        contents = await file.read()
        # 1. predict
        result = predict_from_bytes(contents)
        # 2. save image
        image_path = save_resized_image(contents)
        # 3. save DB
        report = Prediction(
            user_id=user_id,
            image_path=image_path,
            label=result["label"],
            confidence=result["confidence"]
        )
        return Prediction.create_predict(db,report)

    @staticmethod
    def get_predicts(db:Session):
        return Prediction.get_predicts(db)

    @staticmethod
    def delete_predict(db: Session, predict_id: int):
        predict = Prediction.get_predict_by_id(db, predict_id)
        PreRepository.delete_predict(db, predict_id)
        return {"message": "Prediction deleted"}
        
    @staticmethod
    async def get_prediction_detail(db: Session, predict_id: int, user_id: int):
        predict = PredictRepository.get_predict_by_id(db, predict_id)
        if not predict or predict.user_id != user_id:
            raise HTTPException(status_code=404, detail="Prediction not found")
        return predict
