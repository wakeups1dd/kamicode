import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from typing import List

from app.models.problem import Problem
from app.models.submission import Submission
from app.schemas.submission import SubmissionCreate
from app.services.sandbox import get_sandbox
from app.services.ai_analysis_service import AIAnalysisService
from app.engines.rating_tasks import update_user_rating_task
from app.engines.achievement_tasks import process_achievement_event_task
from app.core.websocket import manager

class SubmissionService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.sandbox = get_sandbox()

    async def create_submission(self, user_id: str, data: SubmissionCreate) -> Submission:
        # 1. Fetch problem
        result = await self.db.execute(select(Problem).where(Problem.id == data.problem_id))
        problem = result.scalar_one_or_none()
        if not problem:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Problem not found"
            )

        # 2. Extract test cases
        test_cases = problem.test_cases.get("sample", []) + problem.test_cases.get("hidden", [])
        
        # 3. Execute in Sandbox
        exec_result = await self.sandbox.execute(
            code=data.code,
            language=data.language,
            test_cases=test_cases
        )

        # 4. Save Submission to DB
        new_submission = Submission(
            user_id=user_id,
            problem_id=data.problem_id,
            code=data.code,
            language=data.language,
            verdict=exec_result.verdict,
            runtime_ms=exec_result.runtime_ms,
            memory_kb=exec_result.memory_kb,
            passed_count=exec_result.passed_count,
            total_count=exec_result.total_count,
            is_daily=(problem.daily_date is not None)
        )
        
        self.db.add(new_submission)
        await self.db.commit()
        await self.db.refresh(new_submission)
        
        # 5. Trigger AI Analysis if accepted (runs as asyncio background task within uvicorn's loop)
        if new_submission.verdict == "accepted":
            async def _run_analysis(sub_id: str):
                from app.core.database import async_session_maker
                from app.services.ai_analysis_service import AIAnalysisService
                async with async_session_maker() as analysis_db:
                    service = AIAnalysisService(analysis_db)
                    await service.analyze_submission(sub_id)

            asyncio.create_task(_run_analysis(new_submission.id))

            try:
                # Achievement: submission.accepted
                process_achievement_event_task.delay("submission.accepted", {
                    "user_id": user_id,
                    "submission_id": new_submission.id,
                    "problem_id": new_submission.problem_id
                })
            except Exception as e:
                print(f"⚠️ Failed to enqueue achievement: {e}")
        
        # 6. Trigger Rating Update
        try:
            update_user_rating_task.delay(new_submission.user_id, new_submission.id)
        except Exception as e:
            print(f"⚠️ Failed to enqueue rating update: {e}")
        
        # 7. Broadcast Solve Event
        if new_submission.verdict == "accepted":
            asyncio.create_task(manager.broadcast({
                "type": "ACTIVITY_SOLVE",
                "data": {
                    "username": "User", # In a real app, fetch the username
                    "problem_title": problem.title,
                    "accuracy": f"{int((new_submission.passed_count / new_submission.total_count) * 100)}%",
                    "timestamp": "Just now"
                }
            }))

        return new_submission

    async def get_submission(self, submission_id: str) -> Submission:
        result = await self.db.execute(select(Submission).where(Submission.id == submission_id))
        submission = result.scalar_one_or_none()
        if not submission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Submission not found"
            )
        return submission

    async def get_user_submissions(self, user_id: str, problem_id: str = None) -> List[Submission]:
        query = select(Submission).where(Submission.user_id == user_id)
        if problem_id:
            query = query.where(Submission.problem_id == problem_id)
        
        result = await self.db.execute(query.order_by(Submission.created_at.desc()))
        return result.scalars().all()
