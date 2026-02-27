from sqlalchemy import String, Integer, Boolean, ForeignKey, JSON, DateTime, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid

from app.models.base import Base, TimestampMixin

def generate_uuid() -> str:
    return str(uuid.uuid4())

class RushPuzzle(TimestampMixin, Base):
    """
    Individual puzzles for the Rush mode.
    """
    __tablename__ = "rush_puzzles"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=generate_uuid,
    )
    # MCQ, FILL_BLANK, CODE_OUTPUT, TRACE_OUTPUT
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, default=1)  # 1-5
    
    # content: { "question": "...", "options": [...], "answer": "...", "code_snippet": "..." }
    content: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)
    explanation: Mapped[Optional[str]] = mapped_column(String(1000))
    tags: Mapped[Optional[List[str]]] = mapped_column(JSON)

class RushSession(TimestampMixin, Base):
    """
    A single game session for a user.
    """
    __tablename__ = "rush_sessions"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=generate_uuid,
    )
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    
    # blitz (3m), endurance (3 lives), sudden_death (1 life)
    mode: Mapped[str] = mapped_column(String(20), default="blitz")
    status: Mapped[str] = mapped_column(String(20), default="active")  # active, completed
    
    current_score: Mapped[int] = mapped_column(Integer, default=0)
    current_streak: Mapped[int] = mapped_column(Integer, default=0)
    max_streak: Mapped[int] = mapped_column(Integer, default=0)
    lives_remaining: Mapped[int] = mapped_column(Integer, default=3)
    
    start_rating: Mapped[float] = mapped_column(Float)
    rating_change: Mapped[Optional[float]] = mapped_column(Float)
    
    ended_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    # Relationships
    user: Mapped["User"] = relationship()
    attempts: Mapped[List["RushAttempt"]] = relationship(back_populates="session")

class RushAttempt(TimestampMixin, Base):
    """
    A single answer attempt within a session.
    """
    __tablename__ = "rush_attempts"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=generate_uuid,
    )
    session_id: Mapped[str] = mapped_column(String(36), ForeignKey("rush_sessions.id"), nullable=False, index=True)
    puzzle_id: Mapped[str] = mapped_column(String(36), ForeignKey("rush_puzzles.id"), nullable=False)
    
    user_answer: Mapped[str] = mapped_column(String(500), nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)
    time_taken_ms: Mapped[int] = mapped_column(Integer)
    
    # Relationships
    session: Mapped["RushSession"] = relationship(back_populates="attempts")
    puzzle: Mapped["RushPuzzle"] = relationship()
