from sqlalchemy import String, DateTime, Boolean, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from datetime import datetime
import uuid

from app.models.base import Base, TimestampMixin

def generate_uuid() -> str:
    return str(uuid.uuid4())

class Season(TimestampMixin, Base):
    __tablename__ = "seasons"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=generate_uuid,
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(String(500))
    
    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    status: Mapped[str] = mapped_column(String(20), default="upcoming")  # upcoming, active, completed
    
    # Relationships
    participants: Mapped[List["SeasonParticipant"]] = relationship(back_populates="season")

class SeasonParticipant(TimestampMixin, Base):
    """
    Archived performance of a user at the end of a season.
    """
    __tablename__ = "season_participants"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=generate_uuid,
    )
    season_id: Mapped[str] = mapped_column(String(36), ForeignKey("seasons.id"), nullable=False, index=True)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    
    final_rating: Mapped[float] = mapped_column(Float, nullable=False)
    final_rd: Mapped[float] = mapped_column(Float, nullable=False)
    final_tier: Mapped[str] = mapped_column(String(20), nullable=False)
    final_rank: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Relationships
    season: Mapped["Season"] = relationship(back_populates="participants")
    user: Mapped["User"] = relationship()
