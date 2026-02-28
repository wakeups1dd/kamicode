from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.problem_generator import ProblemGenerator
from app.schemas.problem import ProblemResponse
from app.core.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/problems/generate", response_model=ProblemResponse)
# ... line 12-25 unchanged ...

