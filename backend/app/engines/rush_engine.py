"""
KamiCode — Rush Engine

Logic for fast-paced puzzle sessions, streaks, and lives.
"""

import random
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func

from app.models.rush import RushPuzzle, RushSession, RushAttempt
from app.models.user import User
from app.engines.achievement_tasks import process_achievement_event_task

class RushEngine:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def start_session(self, user_id: str, mode: str = "blitz") -> Dict[str, Any]:
        """
        Starts a new Rush session for a user.
        """
        # 1. Fetch user to get current rating
        result = await self.db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise ValueError("User not found")

        # 2. Set mode specifics
        lives = 3
        if mode == "sudden_death":
            lives = 1
        elif mode == "endurance":
            lives = 3
        
        # 3. Create session
        session = RushSession(
            user_id=user_id,
            mode=mode,
            status="active",
            lives_remaining=lives,
            start_rating=user.blitz_rating,
            current_score=0,
            current_streak=0,
            max_streak=0
        )
        self.db.add(session)
        await self.db.flush() # Get ID

        # 4. Get first puzzle
        puzzle = await self.get_next_puzzle(difficulty=1)
        
        await self.db.commit()
        await self.db.refresh(session)
        
        return {
            "session": session,
            "first_puzzle": puzzle
        }

    async def submit_answer(self, session_id: str, puzzle_id: str, user_answer: str) -> Dict[str, Any]:
        """
        Submits an answer for a puzzle in an active session.
        """
        # 1. Fetch session and puzzle
        result = await self.db.execute(
            select(RushSession).where(RushSession.id == session_id, RushSession.status == "active")
        )
        session = result.scalar_one_or_none()
        if not session:
            return {"error": "Session not found or already completed"}

        result = await self.db.execute(select(RushPuzzle).where(RushPuzzle.id == puzzle_id))
        puzzle = result.scalar_one_or_none()
        if not puzzle:
            return {"error": "Puzzle not found"}

        # 2. Check correctness
        correct_answer = str(puzzle.content.get("answer")).lower().strip()
        is_correct = user_answer.lower().strip() == correct_answer

        # 3. Create attempt
        attempt = RushAttempt(
            session_id=session_id,
            puzzle_id=puzzle_id,
            user_answer=user_answer,
            is_correct=is_correct,
            time_taken_ms=0 # TODO: Pass from client if needed
        )
        self.db.add(attempt)

        # 4. Update session state
        if is_correct:
            session.current_score += 1
            session.current_streak += 1
            if session.current_streak > session.max_streak:
                session.max_streak = session.current_streak
        else:
            session.current_streak = 0
            session.lives_remaining -= 1

        # 5. Check if session should end
        should_end = False
        if session.lives_remaining <= 0:
            should_end = True
        
        if should_end:
            return await self.end_session(session_id)

        # 6. Get next puzzle (difficulty scale based on score)
        # 0-5: diff 1, 6-15: diff 2, 16-30: diff 3, 31-50: diff 4, 51+: diff 5
        target_diff = 1
        if session.current_score > 50: target_diff = 5
        elif session.current_score > 30: target_diff = 4
        elif session.current_score > 15: target_diff = 3
        elif session.current_score > 5: target_diff = 2

        next_puzzle = await self.get_next_puzzle(target_diff)
        
        await self.db.commit()
        await self.db.refresh(session)

        return {
            "is_correct": is_correct,
            "correct_answer": correct_answer if not is_correct else None,
            "current_score": session.current_score,
            "current_streak": session.current_streak,
            "lives_remaining": session.lives_remaining,
            "next_puzzle": next_puzzle,
            "status": session.status
        }

    async def end_session(self, session_id: str) -> Dict[str, Any]:
        """
        Ends a session and calculates rating change.
        """
        result = await self.db.execute(select(RushSession).where(RushSession.id == session_id))
        session = result.scalar_one_or_none()
        if not session or session.status == "completed":
            return {"error": "Session not found or already ended"}

        session.status = "completed"
        session.ended_at = datetime.now(timezone.utc)
        
        # Simplified Rating Change for Blitz
        # rating_change = (score * 5) - 5
        # In a real Glicko-2 implementation, we would treat the session as a series of matches.
        # For now, let's use a simple heuristic.
        rating_change = float(session.current_score * 2) 
        session.rating_change = rating_change

        # Update user's blitz rating
        result = await self.db.execute(select(User).where(User.id == session.user_id))
        user = result.scalar_one_or_none()
        if user:
            user.blitz_rating += rating_change
            # Update RD (slightly decrease since they played)
            user.blitz_rd = max(30.0, user.blitz_rd - 1.0)
        
        await self.db.commit()
        await self.db.refresh(session)

        # 8. Trigger Achievement: rush.completed
        try:
            process_achievement_event_task.delay("rush.completed", {
                "user_id": session.user_id,
                "session_id": session_id,
                "streak": session.max_streak,
                "score": session.current_score
            })
        except Exception as e:
            print(f"⚠️ Failed to enqueue rush achievement: {e}")

        return {
            "is_correct": False,  # Called when wrong answer ends session
            "correct_answer": None,
            "current_score": session.current_score,
            "current_streak": session.current_streak,
            "lives_remaining": session.lives_remaining,
            "next_puzzle": None,
            "status": session.status,
            "message": "Session completed",
            "final_score": session.current_score,
            "max_streak": session.max_streak,
            "rating_change": rating_change,
        }

    async def get_next_puzzle(self, difficulty: int) -> RushPuzzle:
        """
        Picks a random puzzle from the pool matching the difficulty.
        """
        result = await self.db.execute(
            select(RushPuzzle).where(RushPuzzle.difficulty == difficulty).order_by(func.random()).limit(1)
        )
        puzzle = result.scalar_one_or_none()
        
        # Fallback if no puzzle of that difficulty exists
        if not puzzle:
            result = await self.db.execute(select(RushPuzzle).order_by(func.random()).limit(1))
            puzzle = result.scalar_one_or_none()
            
        if not puzzle:
            # Create a mock puzzle if none exist in DB (for initial testing)
            puzzle = RushPuzzle(
                type="MCQ",
                difficulty=1,
                content={
                    "question": "What is the time complexity of Binary Search?",
                    "options": ["O(n)", "O(log n)", "O(n^2)", "O(1)"],
                    "answer": "O(log n)"
                }
            )
            self.db.add(puzzle)
            await self.db.flush()
        
        return puzzle
