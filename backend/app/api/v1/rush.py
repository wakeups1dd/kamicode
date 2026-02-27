from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.rush import (
    RushStartRequest, 
    RushStartResponse, 
    RushAnswerRequest, 
    RushAnswerResponse,
    RushSessionResponse
)
from app.engines.rush_engine import RushEngine

router = APIRouter(prefix="/rush", tags=["Rush"])

@router.post("/start", response_model=RushStartResponse)
async def start_rush_session(
    data: RushStartRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Starts a new Rush game session."""
    engine = RushEngine(db)
    result = await engine.start_session(current_user.id, data.mode)
    return result

@router.post("/sessions/{session_id}/answer", response_model=RushAnswerResponse)
async def submit_rush_answer(
    session_id: str,
    data: RushAnswerRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Submits an answer and returns the next puzzle if the session is still active."""
    engine = RushEngine(db)
    result = await engine.submit_answer(session_id, data.puzzle_id, data.user_answer)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.get("/sessions/{session_id}", response_model=RushSessionResponse)
async def get_rush_session(
    session_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieves the details/status of a specific Rush session."""
    from sqlalchemy import select
    from app.models.rush import RushSession
    result = await db.execute(select(RushSession).where(RushSession.id == session_id))
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session
