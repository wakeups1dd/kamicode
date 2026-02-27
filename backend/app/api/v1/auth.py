"""
KamiCode — Auth API Routes

Endpoints for user registration, login, profile, and wallet linking.
"""

from fastapi import APIRouter, HTTPException, status

from app.core.deps import CurrentUser, DbSession
from app.schemas.auth import (
    TokenResponse,
    UserLogin,
    UserRegister,
    UserResponse,
    WalletLinkRequest,
)
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new account with username, email, and password. Returns a JWT access token.",
)
async def register(data: UserRegister, db: DbSession):
    try:
        user = await AuthService.register_user(db, data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )

    token = AuthService.create_user_token(user)
    return TokenResponse(
        access_token=token,
        user=UserResponse.model_validate(user),
    )


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login with credentials",
    description="Authenticate with email and password. Returns a JWT access token.",
)
async def login(data: UserLogin, db: DbSession):
    user = await AuthService.authenticate_user(db, data)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = AuthService.create_user_token(user)
    return TokenResponse(
        access_token=token,
        user=UserResponse.model_validate(user),
    )


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user profile",
    description="Returns the authenticated user's profile data.",
)
async def get_me(current_user: CurrentUser):
    return UserResponse.model_validate(current_user)


@router.post(
    "/wallet/link",
    response_model=UserResponse,
    summary="Link a crypto wallet",
    description="Link an Ethereum wallet address to the authenticated user's account.",
)
async def link_wallet(
    data: WalletLinkRequest,
    current_user: CurrentUser,
    db: DbSession,
):
    try:
        user = await AuthService.link_wallet(db, current_user, data.wallet_address)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )

    return UserResponse.model_validate(user)
