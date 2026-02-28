"""
KamiCode — Auth Service

Business logic for user registration, authentication, and wallet linking.
"""

import uuid
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class AuthService:
    """Handles user identity functions that supplement Supabase."""

    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: uuid.UUID) -> Optional[User]:
        """Fetch a single user by their UUID."""
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def link_wallet(
        db: AsyncSession, user: User, wallet_address: str
    ) -> User:
        """
        Link a crypto wallet to the user's account.

        Args:
            db: Database session.
            user: The authenticated user.
            wallet_address: The Ethereum wallet address to link.

        Returns:
            Updated User instance.

        Raises:
            ValueError: If the wallet is already linked to another account.
        """
        # Check if wallet is already linked to another user
        existing = await db.execute(
            select(User).where(
                User.wallet_address == wallet_address,
                User.id != user.id,
            )
        )
        if existing.scalar_one_or_none():
            raise ValueError("Wallet already linked to another account")

        user.wallet_address = wallet_address
        await db.flush()
        return user
