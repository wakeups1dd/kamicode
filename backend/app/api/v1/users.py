from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.rating_history import RatingHistory
from app.schemas.rating import RatingHistoryResponse

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
