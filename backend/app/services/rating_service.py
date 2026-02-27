from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from app.models.user import User
from app.models.problem import Problem
from app.models.submission import Submission
from app.models.rating_history import RatingHistory
from app.engines.glicko2 import Glicko2
from app.engines.league_engine import LeagueEngine
from app.engines.achievement_tasks import process_achievement_event_task

class RatingEngine:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.glicko = Glicko2()
        self.league = LeagueEngine()

    async def update_user_rating(self, user_id: str, submission_id: str) -> Optional[RatingHistory]:
        """
        Process a submission and update the user's rating based on difficulty and performance.
        """
        # 1. Fetch data
        result = await self.db.execute(
            select(User, Submission, Problem)
            .join(Submission, User.id == Submission.user_id)
            .join(Problem, Submission.problem_id == Problem.id)
            .where(Submission.id == submission_id, User.id == user_id)
        )
        data = result.one_or_none()
        if not data:
            return None
        
        user, submission, problem = data

        # 2. Determine Problem "Rating" and "RD" based on difficulty
        # In this simplified model, each difficulty has a baseline rating.
        difficulty_mapping = {
            "easy": (1000, 200),
            "medium": (1500, 150),
            "hard": (2000, 100)
        }
        opp_rating, opp_rd = difficulty_mapping.get(problem.difficulty.lower(), (1200, 200))

        # 3. Determine actual score
        actual_score = 1.0 if submission.verdict == "accepted" else 0.0

        # 4. Use Glicko-2 to calculate new parameters
        # Select appropriate rating/rd based on context (default to classical for now)
        old_rating = user.classical_rating
        old_rd = user.classical_rd
        
        new_rating, new_rd, new_vol = self.glicko.calculate_new_rating(
            rating=old_rating,
            rd=old_rd,
            volatility=user.volatility,
            opponent_rating=opp_rating,
            opponent_rd=opp_rd,
            actual_score=actual_score
        )

        # 5. Update User
        change = new_rating - old_rating
        user.classical_rating = new_rating
        user.classical_rd = new_rd
        user.volatility = new_vol

        # 6. Process Tier Change (Promotion/Demotion)
        self.league.process_tier_change(user, new_rating)

        # 7. Create Rating History record
        history = RatingHistory(
            user_id=user_id,
            submission_id=submission_id,
            old_rating=old_rating,
            new_rating=new_rating,
            rating_change=change,
            old_deviation=old_rd,
            new_deviation=new_rd,
            context="classical"
        )
        self.db.add(history)
        
        await self.db.commit()
        await self.db.refresh(history)
        
        # 8. Trigger Achievement: rating.updated
        try:
            process_achievement_event_task.delay("rating.updated", {
                "user_id": user_id,
                "submission_id": submission_id,
                "new_rating": new_rating,
                "tier": user.league_tier
            })
        except Exception as e:
            print(f"⚠️ Failed to enqueue rating achievement: {e}")
        
        return history
