"""
KamiCode — User Model

Core user entity with ratings, league tier, and wallet support.
"""

import uuid

from sqlalchemy import Boolean, Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


def generate_uuid() -> str:
    """Generate a UUID4 string for use as a primary key."""
    return str(uuid.uuid4())


class User(TimestampMixin, Base):
    """Represents a registered KamiCode user."""

    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=generate_uuid,
    )
    username: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )
    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )

    # ─── Wallet ────────────────────────────────────────────────────
    wallet_address: Mapped[str | None] = mapped_column(
        String(42), unique=True, nullable=True
    )

    # ─── Competitive Stats ─────────────────────────────────────────
    classical_rating: Mapped[float] = mapped_column(Float, default=1200.0)
    classical_rd: Mapped[float] = mapped_column(Float, default=350.0)  # Rating Deviation
    
    blitz_rating: Mapped[float] = mapped_column(Float, default=1200.0)
    blitz_rd: Mapped[float] = mapped_column(Float, default=350.0)
    
    volatility: Mapped[float] = mapped_column(Float, default=0.06)
    
    league_tier: Mapped[str] = mapped_column(String(20), default="bronze")

    # ─── Account Status ────────────────────────────────────────────
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # ─── Relationships (populated in later phases) ─────────────────
    # submissions = relationship("Submission", back_populates="user", lazy="selectin")
    # achievements = relationship("UserAchievement", back_populates="user", lazy="selectin")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username={self.username}, tier={self.league_tier})>"
