from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.submission import SubmissionCreate, SubmissionResponse
from app.schemas.ai_analysis import AIAnalysisResponse
from app.services.submission_service import SubmissionService
from app.services.ai_analysis_service import AIAnalysisService

router = APIRouter(prefix="/submissions", tags=["submissions"])

@router.post("", response_model=SubmissionResponse, status_code=status.HTTP_201_CREATED)
async def create_submission(
    data: SubmissionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Submit code for evaluation against a problem's test cases.
    """
    service = SubmissionService(db)
    return await service.create_submission(current_user.id, data)

@router.get("/{submission_id}", response_model=SubmissionResponse)
async def get_submission(
    submission_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get details and verdict for a specific submission.
    """
    service = SubmissionService(db)
    submission = await service.get_submission(submission_id)
    
    # Only allow users to see their own submissions (could be relaxed later for public profile)
    if submission.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this submission")
        
    return submission

@router.get("", response_model=List[SubmissionResponse])
async def list_my_submissions(
    problem_id: str = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List all submissions for the current user, optionally filtered by problem.
    """
    service = SubmissionService(db)
    return await service.get_user_submissions(current_user.id, problem_id)

@router.get("/{submission_id}/analysis", response_model=AIAnalysisResponse)
async def get_submission_analysis(
    submission_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get the AI analysis for a specific submission.
    """
    service = AIAnalysisService(db)
    analysis = await service.get_analysis_by_submission(submission_id)
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found or still processing"
        )
    return analysis
