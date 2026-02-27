from sqlalchemy import String, ForeignKey, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
import uuid
from datetime import datetime

from app.models.base import Base, TimestampMixin

def generate_uuid() -> str:
    return str(uuid.uuid4())

class UserAchievement(TimestampMixin, Base):
    """
    Achievements earned by users, potentially mintable as NFTs.
    """
    __tablename__ = "user_achievements"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=generate_uuid,
    )
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    achievement_type: Mapped[str] = mapped_column(String(50), nullable=False) # e.g. FIRST_SOLVER
    
    # Context IDs
    trigger_id: Mapped[Optional[str]] = mapped_column(String(36)) # submission_id, session_id, etc.
    season_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("seasons.id"))
    
    # NFT Data (filled after minting)
    nft_token_id: Mapped[Optional[int]] = mapped_column(Integer)
    nft_tx_hash: Mapped[Optional[str]] = mapped_column(String(66))
    metadata_uri: Mapped[Optional[str]] = mapped_column(String(200)) # IPFS URI
    
    # Relationships
    user: Mapped["User"] = relationship()
    season: Mapped[Optional["Season"]] = relationship()
