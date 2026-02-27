from celery import Celery
from app.core.config import get_settings

settings = get_settings()

celery_app = Celery(
    "kamicode",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.engines.analysis_tasks", "app.engines.rating_tasks", "app.engines.achievement_tasks", "app.engines.problem_tasks"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Kolkata",
    enable_utc=True,
    task_always_eager=True,
    task_eager_propagates=True
)

from celery.schedules import crontab

celery_app.conf.beat_schedule = {
    "generate-daily-problem-midnight-ist": {
        "task": "app.engines.problem_tasks.generate_daily_problem_task",
        "schedule": crontab(hour=0, minute=0), # Midnight IST every day
    },
}
