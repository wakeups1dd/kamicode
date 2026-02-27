from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import yaml
import os

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.achievement import UserAchievement
from app.schemas.achievement import AchievementResponse, AchievementCatalogItem

router = APIRouter(prefix="/achievements", tags=["Achievements"])

def load_definitions():
    path = os.path.join(os.path.dirname(__file__), "..", "..", "engines", "achievement_definitions.yaml")
    with open(path, "r") as f:
        return yaml.safe_load(f)

@router.get("/me", response_model=List[AchievementResponse])
async def list_my_achievements(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all achievements earned by the current user."""
    result = await db.execute(
        select(UserAchievement)
        .where(UserAchievement.user_id == current_user.id)
        .order_by(UserAchievement.created_at.desc())
    )
    return result.scalars().all()

@router.get("/catalog", response_model=List[AchievementCatalogItem])
async def get_achievement_catalog(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get the full list of possible achievements and current user's status."""
    definitions = load_definitions()
    
    # Get user's earned achievements
    result = await db.execute(
        select(UserAchievement)
        .where(UserAchievement.user_id == current_user.id)
    )
    earned = {a.achievement_type: a for a in result.scalars().all()}
    
    catalog = []
    for item in definitions.get("achievements", []):
        earned_info = earned.get(item["id"])
        catalog.append(AchievementCatalogItem(
            id=item["id"],
            name=item["name"],
            description=item["description"],
            earned=earned_info is not None,
            earned_at=earned_info.created_at if earned_info else None,
            nft_status="minted" if earned_info and earned_info.nft_token_id else ("pending" if earned_info and earned_info.nft_tx_hash else "none")
        ))
    
    return catalog
