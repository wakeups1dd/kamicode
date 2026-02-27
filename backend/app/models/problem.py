from sqlalchemy import String, Text, Date, JSON
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional, List
import uuid

from app.models.base import Base, TimestampMixin

def generate_uuid() -> str:
    return str(uuid.uuid4())

class Problem(TimestampMixin, Base):
    __tablename__ = "problems"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=generate_uuid,
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[str] = mapped_column(String(200), unique=True, nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    difficulty: Mapped[str] = mapped_column(String(10), nullable=False)  # easy, medium, hard
    
    # test_cases: { "sample": [{"input": "...", "expected": "..."}], "hidden": [...] }
    test_cases: Mapped[dict] = mapped_column(JSON, nullable=False)
    
    constraints: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Store tags as a JSON list for SQLite compatibility while remaining JSONB-ready for PG
    tags: Mapped[List[str]] = mapped_column(JSON, default=list)
    
    generated_by: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    daily_date: Mapped[Optional[str]] = mapped_column(Date, nullable=True, unique=True)
