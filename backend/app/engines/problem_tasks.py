import asyncio
import logging
from datetime import date
from app.core.celery_app import celery_app
from app.core.database import async_session_maker
from app.services.problem_generator import ProblemGenerator

logger = logging.getLogger(__name__)

async def _run_generate_daily_problem():
    logger.info("Starting automated daily problem generation...")
    async with async_session_maker() as db:
        generator = ProblemGenerator(db)
        
        # We'll use "medium" difficulty for standard daily challenges.
        # This could be randomized in the future.
        problem = await generator.generate_daily_problem(difficulty="medium")
        
        if problem:
            today = date.today()
            # The ProblemGenerator calls ProblemService.create_problem
            # We now need to update it to be today's daily problem
            
            # First, clear any existing problem for today to avoid UNIQUE constraint failed
            from sqlalchemy import update
            from app.models.problem import Problem
            await db.execute(update(Problem).where(Problem.daily_date == today).values(daily_date=None))
            
            problem.daily_date = today
            await db.commit()
            logger.info(f"✅ Successfully generated and assigned daily problem: '{problem.title}' for {today}")
        else:
            logger.error("❌ Failed to generate daily problem from AI.")

@celery_app.task(name="app.engines.problem_tasks.generate_daily_problem_task")
def generate_daily_problem_task():
    """
    Celery task that orchestrates the async generation of a new daily coding problem.
    """
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    loop.run_until_complete(_run_generate_daily_problem())
