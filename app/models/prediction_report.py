from sqlalchemy import Column,DateTime, Integer,String,ForeignKey,Float
from datetime import datetime

from app.db.base import Base
class Prediction(Base):
    __tablename__ = "prediction_reports"

    id = Column(Integer,primary_key =True)

    user_id = Column(Integer,ForeignKey("users.id"))

    image_path = Column(String)
    label = Column(String)
    confidence = Column(Float, nullable=False)

    created_at = Column(DateTime,default=datetime.utcnow)