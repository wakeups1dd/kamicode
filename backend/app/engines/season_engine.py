"""
KamiCode — Season Engine

Manages competition cycles, seasonal rating resets, and archiving performance.
"""

from typing import Optional, List
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func
from app.models.season import Season, SeasonParticipant
from app.models.user import User
from app.engines.league_engine import TIER_THRESHOLDS
from app.engines.achievement_tasks import process_achievement_event_task

class SeasonEngine:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_season(self, name: str, start_date: datetime, end_date: datetime) -> Season:
        """Creates a new season."""
        slug = name.lower().replace(" ", "-")
        season = Season(
            name=name,
            slug=slug,
            start_date=start_date,
            end_date=end_date,
            status="upcoming"
        )
        self.db.add(season)
        await self.db.commit()
        await self.db.refresh(season)
        return season

    async def start_season(self, season_id: str):
        """Marks a season as active."""
        await self.db.execute(
            update(Season)
            .where(Season.id == season_id)
            .values(status="active", is_active=True)
        )
        # Deactivate other seasons (simplified)
        await self.db.execute(
            update(Season)
            .where(Season.id != season_id)
            .values(is_active=False)
        )
        await self.db.commit()

    async def end_season(self, season_id: str):
        """
        Completes a season, archives participants, and resets ratings.
        """
        # 1. Fetch the season
        result = await self.db.execute(select(Season).where(Season.id == season_id))
        season = result.scalar_one_or_none()
        if not season:
            return

        # 2. Mark season as completed
        season.status = "completed"
        season.is_active = False

        # 3. Archive all active users as participants
        users_result = await self.db.execute(select(User).where(User.is_active == True))
        users = users_result.scalars().all()

        for user in users:
            participant = SeasonParticipant(
                season_id=season_id,
                user_id=user.id,
                final_rating=user.classical_rating,
                final_rd=user.classical_rd,
                final_tier=user.league_tier,
                # Initial rank can be calculated later or set here if desired
            )
            self.db.add(participant)

            # 4. Soft Reset Ratings
            # new_rating = floor + (old - floor) * 0.6
            floor = TIER_THRESHOLDS.get(user.league_tier.lower(), 0.0)
            new_rating = floor + (user.classical_rating - floor) * 0.6
            
            user.classical_rating = new_rating
            # Rating deviation (RD) is reset to a higher value for the new season
            user.classical_rd = 350.0  # Resetting to default for fresh assessment

        await self.db.commit()

        # 5. Trigger Achievement: season.ended for all participants
        for user in users:
            try:
                process_achievement_event_task.delay("season.ended", {
                    "user_id": user.id,
                    "season_id": season_id,
                    "season_slug": season.slug
                })
            except Exception as e:
                print(f"⚠️ Failed to enqueue season achievement for user {user.id}: {e}")

    def get_tier_floor(self, tier: str) -> float:
        return TIER_THRESHOLDS.get(tier.lower(), 0.0)
