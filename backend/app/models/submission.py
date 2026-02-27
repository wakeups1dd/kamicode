from sqlalchemy import String, Text, Integer, Boolean, ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
import uuid

from app.models.base import Base, TimestampMixin

def generate_uuid() -> str:
    return str(uuid.uuid4())

class Submission(TimestampMixin, Base):
    __tablename__ = "submissions"

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
    problem_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("problems.id"),
        nullable=False,
        index=True
    )
    code: Mapped[str] = mapped_column(Text, nullable=False)
    language: Mapped[str] = mapped_column(String(20), nullable=False)  # python, javascript, etc.
    
    verdict: Mapped[str] = mapped_column(String(20), nullable=False)  # accepted, wrong_answer, tle, mle, runtime_error
    runtime_ms: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    memory_kb: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    passed_count: Mapped[int] = mapped_column(Integer, default=0)
    total_count: Mapped[int] = mapped_column(Integer, default=0)
    
    # AI Analysis ID (Self-referential or forward reference handled later in Phase 3)
    ai_analysis_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    
    is_daily: Mapped[bool] = mapped_column(Boolean, default=False)
