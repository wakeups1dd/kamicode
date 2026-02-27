from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from datetime import datetime

from app.core.database import get_db
from app.schemas.season import SeasonCreate, SeasonResponse
from app.engines.season_engine import SeasonEngine
from app.core.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/seasons", tags=["Seasons"])

@router.post("", response_model=SeasonResponse, status_code=status.HTTP_201_CREATED)
async def create_season(
    data: SeasonCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new season (Admin only in production)."""
    # For now, anyone can create for testing
    engine = SeasonEngine(db)
    return await engine.create_season(data.name, data.start_date, data.end_date)

@router.post("/{season_id}/start")
async def start_season(
    season_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Start a season."""
    engine = SeasonEngine(db)
    await engine.start_season(season_id)
    return {"message": "Season started"}

@router.post("/{season_id}/end")
async def end_season(
    season_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """End a season and trigger soft-resets."""
    engine = SeasonEngine(db)
    await engine.end_season(season_id)
    return {"message": "Season ended and ratings reset"}

@router.get("", response_model=List[SeasonResponse])
async def list_seasons(db: AsyncSession = Depends(get_db)):
    """List all seasons."""
    from sqlalchemy import select
    from app.models.season import Season
    result = await db.execute(select(Season).order_by(Season.start_date.desc()))
    return result.scalars().all()
