from pydantic import BaseModel, ConfigDict
from datetime import datetime

class ReportResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    label: str
    image_path: str
    confidence: float
    created_at: datetime
