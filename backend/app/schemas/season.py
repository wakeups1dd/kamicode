from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class SeasonBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)

class SeasonCreate(SeasonBase):
    start_date: datetime
    end_date: datetime

class SeasonResponse(SeasonBase):
    id: str
    slug: str
    start_date: datetime
    end_date: datetime
    is_active: bool
    status: str

    class Config:
        from_attributes = True

class SeasonParticipantResponse(BaseModel):
    user_id: str
    final_rating: float
    final_rd: float
    final_tier: str
    final_rank: Optional[int] = None

    class Config:
        from_attributes = True
