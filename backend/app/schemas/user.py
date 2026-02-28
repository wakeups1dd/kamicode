"""
KamiCode — User Schemas

Pydantic models for user-related requests and responses.
"""

import re
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class UserResponse(BaseModel):
    """Response schema for user data."""

    id: str
    username: str
    email: str
    wallet_address: Optional[str] = None
    classical_rating: float
    blitz_rating: float
    league_tier: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class WalletLinkRequest(BaseModel):
    """Request schema for linking a crypto wallet."""

    wallet_address: str = Field(
        ...,
        min_length=42,
        max_length=42,
        description="Ethereum wallet address (0x...)",
    )
    signature: str = Field(
        ...,
        description="Signed message proving wallet ownership",
    )

    @field_validator("wallet_address")
    @classmethod
    def validate_wallet(cls, v: str) -> str:
        if not re.match(r"^0x[a-fA-F0-9]{40}$", v):
            raise ValueError("Invalid Ethereum wallet address")
        return v
