from sqlalchemy.orm import Session
from app.models.prediction_report import Prediction

class PredictRepository():
    @staticmethod
    def create_predict(db: Session, report: Prediction):
        db.add(report)
        db.commit()
        db.refresh(report)
        return report

    @staticmethod
    def get_predicts(db: Session):
        return db.query(Prediction).all()

    @staticmethod
    def get_predict_by_id(db: Session, predict_id: int):
        return db.query(Prediction).filter(Prediction.id == predict_id).first()

    @staticmethod
    def delete_predict(db: Session, predict: Prediction):
        return db.delete(predict)
        db.commit()
