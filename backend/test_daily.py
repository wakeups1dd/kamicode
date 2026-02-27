import asyncio
import logging
from app.engines.problem_tasks import _run_generate_daily_problem

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    asyncio.run(_run_generate_daily_problem())
