import os
from celery import Celery
from celery.schedules import crontab
import tasks

# ----------------------------------------------------
# Celery configuration
# ----------------------------------------------------

REDIS_URL = os.environ["REDIS_URL"]  # fail fast if missing

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", REDIS_URL)
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", REDIS_URL)

# ----------------------------------------------------
# Create Celery application
# ----------------------------------------------------

celery = Celery(
    "microfarm_etl",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
)

celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,

    # Important for Render
    broker_connection_retry_on_startup=True,
)

# Autodiscover tasks
celery.autodiscover_tasks(["tasks"])

# ----------------------------------------------------
# Schedule ETL task
# ----------------------------------------------------

celery.conf.beat_schedule = {
    "generate-fake-data-every-minute": {
        "task": "run_etl_task",
        "schedule": 60.0,
    },
}
