from pydantic import BaseModel,EmailStr,Field
from datetime import datetime
class PredictionResponse(BaseModel):
    label:str
    confidence : float

class ReportResponse(BaseModel):
    id: int
    label: str
    image_path:str
    confidence: float
    created_at: datetime

    class Config:
        from_attributes = True
