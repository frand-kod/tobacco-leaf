from sqlalchemy.orm import Session
from app.models.prediction_report import PredictionReport

class PredictRepository():
    @staticmethod
    def create_predict(db: Session, report: PredictionReport):
        db.add(report)
        db.commit()
        db.refresh(report)
        return report

    @staticmethod
    def get_predicts(db: Session):
        return db.query(PredictionReport).all()
    
    @staticmethod
    def get__predict_by_user(db: Session, user_id: int):
        return db.query(PredictionReport)\
            .filter(PredictionReport.user_id == user_id)\
            .order_by(PredictionReport.created_at.desc())\
            .all()

    @staticmethod
    def get_predict_by_id(db: Session, predict_id: int):
        return db.query(PredictionReport).filter(PredictionReport.id == predict_id).first()

    @staticmethod
    def delete_predict(db: Session, predict: PredictionReport):
        db.delete(predict)
        db.commit()
