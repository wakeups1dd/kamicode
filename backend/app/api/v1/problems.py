from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.core.database import get_db
from app.schemas.problem import ProblemResponse, ProblemListResponse, ProblemCreate
from app.services.problem_service import ProblemService
from app.core.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/problems", tags=["problems"])

@router.get("", response_model=List[ProblemListResponse])
async def list_problems(
    difficulty: Optional[str] = None,
    tag: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    List all available coding problems with optional filters.
    """
    service = ProblemService(db)
    return await service.list_problems(difficulty=difficulty, tag=tag)

@router.get("/daily", response_model=Optional[ProblemResponse])
async def get_daily_problem(db: AsyncSession = Depends(get_db)):
    """
    Retrieve today's Daily Challenge problem.
    """
    service = ProblemService(db)
    return await service.get_daily_problem()

@router.get("/{slug}", response_model=ProblemResponse)
async def get_problem(slug: str, db: AsyncSession = Depends(get_db)):
    """
    Get full details for a specific problem by its slug.
    (Hides hidden test cases from the response).
    """
    service = ProblemService(db)
    return await service.get_problem_by_slug(slug)

@router.post("", response_model=ProblemResponse, status_code=status.HTTP_201_CREATED)
async def create_problem(
    data: ProblemCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new problem (Currently open to all logged-in users, will be admin-only).
    """
    service = ProblemService(db)
    return await service.create_problem(data)
