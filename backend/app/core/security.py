"""
KamiCode — Security Utilities

JWT token management for Supabase Auth.
"""

from typing import Any

from jose import JWTError, jwt

from app.core.config import get_settings

settings = get_settings()

def decode_access_token(token: str) -> dict[str, Any]:
    """
    Decode and verify a Supabase Auth JWT access token.

    Args:
        token: The JWT string.

    Returns:
        Decoded payload dictionary.

    Raises:
        JWTError: If the token is invalid or expired.
    """
    # Supabase signs JWTs using the project's JWT Secret and HS256 algorithm.
    # The audience defaults to "authenticated" for logged-in users.
    return jwt.decode(
        token,
        settings.SUPABASE_JWT_SECRET,
        algorithms=["HS256"],
        audience="authenticated"
    )
