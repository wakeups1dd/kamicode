from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from typing import List, Optional
from datetime import date

from app.models.problem import Problem
from app.schemas.problem import ProblemCreate, ProblemUpdate

class ProblemService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_problem(self, data: ProblemCreate) -> Problem:
        # Check if slug exists
        result = await self.db.execute(select(Problem).where(Problem.slug == data.slug))
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Problem with slug '{data.slug}' already exists"
            )

        new_problem = Problem(
            title=data.title,
            slug=data.slug,
            description=data.description,
            difficulty=data.difficulty,
            test_cases=data.test_cases.dict(),
            constraints=data.constraints,
            tags=data.tags
        )
        
        self.db.add(new_problem)
        await self.db.commit()
        await self.db.refresh(new_problem)
        return new_problem

    async def get_problem_by_slug(self, slug: str) -> Problem:
        result = await self.db.execute(select(Problem).where(Problem.slug == slug))
        problem = result.scalar_one_or_none()
        if not problem:
            raise HTTPException(status_code=404, detail="Problem not found")
        return problem

    async def get_daily_problem(self) -> Optional[Problem]:
        today = date.today()
        result = await self.db.execute(select(Problem).where(Problem.daily_date == today))
        return result.scalar_one_or_none()

    async def list_problems(self, difficulty: str = None, tag: str = None) -> List[Problem]:
        query = select(Problem)
        if difficulty:
            query = query.where(Problem.difficulty == difficulty)
        # Note: Tag filtering on JSON array in SQLite is a bit tricky, 
        # but since we have few problems now, we can filter in memory or use basic LIKE
        
        result = await self.db.execute(query.order_by(Problem.created_at.desc()))
        problems = result.scalars().all()
        
        if tag:
            problems = [p for p in problems if tag in (p.tags or [])]
            
        return list(problems)
