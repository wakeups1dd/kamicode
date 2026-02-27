"""
KamiCode — Auth Schemas

Pydantic models for authentication request/response validation.
"""

import re
import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserRegister(BaseModel):
    """Request schema for user registration."""

    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Unique username (3-50 characters, alphanumeric + underscores)",
    )
    email: str = Field(
        ...,
        max_length=255,
        description="Valid email address",
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="Password (8-128 characters)",
    )

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not re.match(r"^[a-zA-Z0-9_]+$", v):
            raise ValueError("Username must contain only letters, numbers, and underscores")
        return v.lower()

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", v):
            raise ValueError("Invalid email address format")
        return v.lower()

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v


class UserLogin(BaseModel):
    """Request schema for user login."""

    email: str = Field(..., description="Email address")
    password: str = Field(..., description="Password")


class TokenResponse(BaseModel):
    """Response schema for authentication tokens."""

    access_token: str
    token_type: str = "bearer"
    user: "UserResponse"


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


# Resolve forward reference
TokenResponse.model_rebuild()
