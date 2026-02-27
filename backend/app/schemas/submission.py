from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid

class SubmissionBase(BaseModel):
    problem_id: str
    code: str
    language: str = Field(..., pattern="^(python|javascript|cpp|java)$")

class SubmissionCreate(SubmissionBase):
    pass

class SubmissionResponse(BaseModel):
    id: str
    problem_id: str
    user_id: str
    language: str
    verdict: str
    runtime_ms: Optional[int] = None
    memory_kb: Optional[int] = None
    passed_count: int
    total_count: int
    is_daily: bool
    created_at: datetime

    class Config:
        from_attributes = True
