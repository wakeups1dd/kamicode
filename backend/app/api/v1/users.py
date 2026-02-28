from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.core.database import get_db
from app.core.deps import get_current_user, CurrentUser, DbSession
from app.models.user import User
from app.models.rating_history import RatingHistory
from app.schemas.rating import RatingHistoryResponse
from app.schemas.user import UserResponse, WalletLinkRequest
from app.services.auth_service import AuthService

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me/ratings", response_model=List[RatingHistoryResponse])
async def get_my_rating_history(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get the rating history for the current authenticated user.
    """
    result = await db.execute(
        select(RatingHistory)
        .where(RatingHistory.user_id == current_user.id)
        .order_by(RatingHistory.created_at.desc())
    )
    return result.scalars().all()


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
