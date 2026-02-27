from sqlalchemy import String, Text, Integer, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
import uuid

from app.models.base import Base, TimestampMixin

def generate_uuid() -> str:
    return str(uuid.uuid4())

class AIAnalysis(TimestampMixin, Base):
    __tablename__ = "ai_analyses"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=generate_uuid,
    )
    submission_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("submissions.id"),
        unique=True,
        nullable=False,
        index=True
    )
    time_complexity: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    space_complexity: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    approach_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    quality_score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # 0-100
    feedback: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    percentile_rank: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    model_used: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
