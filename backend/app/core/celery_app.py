from celery import Celery
from app.core.config import get_settings

settings = get_settings()

celery_app = Celery(
    "kamicode",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.engines.analysis_tasks", "app.engines.rating_tasks"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    # Local fallback for environments without Redis
    task_always_eager=True,
    task_eager_propagates=True
)
