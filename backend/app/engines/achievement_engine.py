"""
KamiCode — Achievement Engine

Evaluates events and awards achievements based on defined rules.
"""

import yaml
import os
from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from datetime import datetime, timedelta

from app.models.achievement import UserAchievement
from app.models.submission import Submission
from app.models.user import User
from app.models.rush import RushSession
from app.models.problem import Problem
from app.models.ai_analysis import AIAnalysis

class AchievementEngine:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.definitions = self._load_definitions()

    def _load_definitions(self) -> Dict[str, Any]:
        path = os.path.join(os.path.dirname(__file__), "achievement_definitions.yaml")
        with open(path, "r") as f:
            return yaml.safe_load(f)

    async def process_event(self, event_type: str, event_data: dict):
        """
        Main entry point for evaluating achievements after an event.
        """
        user_id = event_data.get("user_id")
        if not user_id:
            return

        # Find rules matching the trigger
        matching_rules = [
            rule for rule in self.definitions.get("achievements", [])
            if rule.get("trigger") == event_type
        ]

        for rule in matching_rules:
            achievement_id = rule["id"]
            
            # Check if user already has this achievement
            exists = await self.db.execute(
                select(UserAchievement).where(
                    UserAchievement.user_id == user_id,
                    UserAchievement.achievement_type == achievement_id
                )
            )
            if exists.scalar_one_or_none():
                continue

            # Evaluate conditions
            if await self._evaluate_rule(rule, event_data):
                await self._award_achievement(user_id, achievement_id, event_data)

    async def _evaluate_rule(self, rule: dict, data: dict) -> bool:
        conditions = rule.get("conditions", [])
        for condition in conditions:
            c_type = condition["type"]
            val = condition.get("value")
            
            if c_type == "first_accepted_for_problem":
                # Check if this is the first accepted submission for the problem
                problem_id = data.get("problem_id")
                result = await self.db.execute(
                    select(func.count(Submission.id))
                    .where(Submission.problem_id == problem_id, Submission.verdict == "accepted")
                )
                if result.scalar() != 1: # Counting the one just created
                    return False

            elif c_type == "tier_reaches":
                # User model should already be updated by RatingService/LeagueEngine
                user_id = data.get("user_id")
                result = await self.db.execute(select(User).where(User.id == user_id))
                user = result.scalar_one_or_none()
                if not user or user.league_tier.lower() != val.lower():
                    return False

            elif c_type == "rush_streak_reaches":
                # From rush session data
                streak = data.get("streak", 0)
                if streak < int(val):
                    return False

            elif c_type == "quality_percentile":
                # Check AI analysis percentile
                analysis_id = data.get("analysis_id")
                result = await self.db.execute(select(AIAnalysis).where(AIAnalysis.id == analysis_id))
                analysis = result.scalar_one_or_none()
                if not analysis or (analysis.quality_score_percentile or 0) < int(val):
                    return False

            elif c_type == "streak_reaches":
                # Check daily streak (pseudo-logic for now)
                # In a real app, we'd query the Submissions table for unique days
                pass # TODO: Implement real streak check

        return True

    async def _award_achievement(self, user_id: str, achievement_type: str, data: dict):
        achievement = UserAchievement(
            user_id=user_id,
            achievement_type=achievement_type,
            trigger_id=data.get("trigger_id") or data.get("submission_id") or data.get("session_id"),
            season_id=data.get("season_id")
        )
        self.db.add(achievement)
        await self.db.commit()
        print(f"🏆 Achievement Unlocked: {achievement_type} for User {user_id}")
        
        from app.engines.achievement_tasks import mint_achievement_nft_task
        mint_achievement_nft_task.delay(achievement.id)
