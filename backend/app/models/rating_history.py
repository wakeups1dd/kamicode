from sqlalchemy import String, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from datetime import datetime
import uuid

from app.models.base import Base, TimestampMixin

def generate_uuid() -> str:
    return str(uuid.uuid4())

class RatingHistory(TimestampMixin, Base):
    __tablename__ = "rating_history"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=generate_uuid,
    )
    user_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    # The submission that triggered this rating change (if any)
    submission_id: Mapped[Optional[str]] = mapped_column(
        String(36),
        ForeignKey("submissions.id"),
        nullable=True
    )
    
    old_rating: Mapped[float] = mapped_column(Float, nullable=False)
    new_rating: Mapped[float] = mapped_column(Float, nullable=False)
    rating_change: Mapped[float] = mapped_column(Float, nullable=False)
    
    # Glicko-2 specific parameters
    old_deviation: Mapped[float] = mapped_column(Float, nullable=False)
    new_deviation: Mapped[float] = mapped_column(Float, nullable=False)
    
    # Context (Daily Challenge, Blitz, etc.)
    context: Mapped[str] = mapped_column(String(20), default="classical")
    
    # Optional season reference (Phase 4.3)
    season_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
