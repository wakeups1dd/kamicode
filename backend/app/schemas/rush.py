from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class RushPuzzleResponse(BaseModel):
    id: str
    type: str
    difficulty: int
    content: Dict[str, Any]
    explanation: Optional[str] = None

    class Config:
        from_attributes = True

class RushSessionResponse(BaseModel):
    id: str
    user_id: str
    mode: str
    status: str
    current_score: int
    current_streak: int
    max_streak: int
    lives_remaining: int
    start_rating: float
    rating_change: Optional[float] = None
    created_at: datetime
    ended_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class RushStartRequest(BaseModel):
    mode: str = Field("blitz", description="blitz, endurance, or sudden_death")

class RushStartResponse(BaseModel):
    session: RushSessionResponse
    first_puzzle: RushPuzzleResponse

class RushAnswerRequest(BaseModel):
    puzzle_id: str
    user_answer: str

class RushAnswerResponse(BaseModel):
    is_correct: bool
    correct_answer: Optional[str] = None
    current_score: int
    current_streak: int
    lives_remaining: int
    next_puzzle: Optional[RushPuzzleResponse] = None
    status: str
