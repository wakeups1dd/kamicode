from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.problem_generator import ProblemGenerator
from app.schemas.problem import ProblemResponse
from app.core.deps import get_current_user
from app.models.user import User

from app.services.rush_puzzle_generator import RushPuzzleGenerator

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/problems/generate", response_model=ProblemResponse)
# ... line 12-25 unchanged ...

@router.post("/rush/generate")
async def trigger_rush_generation(
    count: int = 5,
    difficulty: int = 1,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Trigger bulk Rush puzzle generation.
    """
    generator = RushPuzzleGenerator(db)
    try:
        puzzles = await generator.generate_batch(count=count, difficulty=difficulty)
        return {"message": f"Successfully generated {len(puzzles)} puzzles"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
