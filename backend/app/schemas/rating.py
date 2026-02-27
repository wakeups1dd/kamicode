from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RatingHistoryResponse(BaseModel):
    id: str
    user_id: str
    submission_id: Optional[str] = None
    old_rating: float
    new_rating: float
    rating_change: float
    old_deviation: float
    new_deviation: float
    context: str
    created_at: datetime

    class Config:
        from_attributes = True
