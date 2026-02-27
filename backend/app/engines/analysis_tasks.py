import asyncio
from app.core.celery_app import celery_app
from app.core.database import async_session_maker
from app.services.ai_analysis_service import AIAnalysisService

@celery_app.task(name="app.engines.analysis_tasks.analyze_submission_task")
def analyze_submission_task(submission_id: str):
    """
    Background task to analyze a submission.
    """
    async def run_analysis():
        async with async_session_maker() as db:
            service = AIAnalysisService(db)
            await service.analyze_submission(submission_id)

    # Run the async logic in the sync Celery worker
    loop = asyncio.get_event_loop()
    if loop.is_running():
        # This shouldn't happen in a standard Celery worker, but good to handle
        asyncio.create_task(run_analysis())
    else:
        loop.run_until_complete(run_analysis())
