from pydantic import BaseModel
from typing import Optional

class AIAnalysisResponse(BaseModel):
    id: str
    submission_id: str
    time_complexity: Optional[str] = None
    space_complexity: Optional[str] = None
    approach_name: Optional[str] = None
    quality_score: Optional[int] = None
    feedback: Optional[str] = None
    percentile_rank: Optional[float] = None
    model_used: Optional[str] = None

    class Config:
        from_attributes = True
