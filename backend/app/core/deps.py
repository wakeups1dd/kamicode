"""
KamiCode — FastAPI Dependencies

Reusable Depends() callables for route injection.
"""

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.user import User
from app.core.config import get_settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    """
    Extract the current authenticated user from the JWT bearer token.

    Raises:
        HTTPException 401: If the token is invalid, expired, or user not found.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    settings = get_settings()

    # Dev environment auto-login fallback
    if not token and settings.ENVIRONMENT in ["dev", "local"]:
        result = await db.execute(select(User).where(User.username == "devuser"))
        user = result.scalar_one_or_none()
        if user:
            return user

    if not token:
        raise credentials_exception

    try:
        payload = decode_access_token(token)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Supabase manages auth.users, but we need a corresponding row in public.users
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if user is None:
        # First time login/signup -> copy identity into public.users
        email = payload.get("email", "")
        # Create a default username based on email or user_id prefix if not provided
        username = payload.get("user_metadata", {}).get("username")
        if not username:
            username = email.split("@")[0] if email else user_id[:8]

        # Handle duplicate username scenario locally
        base_username = username
        counter = 1
        while True:
            existing = await db.execute(select(User).where(User.username == username))
            if existing.scalar_one_or_none() is None:
                break
            username = f"{base_username}{counter}"
            counter += 1

        user = User(
            id=user_id,
            email=email,
            username=username,
            classical_rating=1200,
            blitz_rating=1200,
            league_tier="bronze",
            is_active=True,
        )
        db.add(user)
        await db.flush()

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is deactivated",
        )

    return user


# Type alias for convenience in route signatures
CurrentUser = Annotated[User, Depends(get_current_user)]
DbSession = Annotated[AsyncSession, Depends(get_db)]
