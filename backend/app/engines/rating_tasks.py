import asyncio
from app.core.celery_app import celery_app
from app.core.database import async_session_maker
from app.services.rating_service import RatingEngine

@celery_app.task(name="app.engines.rating_tasks.update_user_rating_task")
def update_user_rating_task(user_id: str, submission_id: str):
    """
    Background task to update user rating.
    """
    async def run_update():
        async with async_session_maker() as db:
            service = RatingEngine(db)
            await service.update_user_rating(user_id, submission_id)

    loop = asyncio.get_event_loop()
    if loop.is_running():
        asyncio.create_task(run_update())
    else:
        loop.run_until_complete(run_update())
