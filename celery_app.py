import os
from celery import Celery
from celery.schedules import crontab

# ----------------------------------------------------
# Celery configuration
# ----------------------------------------------------

# Broker URL (Redis or RabbitMQ — you choose via env)
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")

# Optional: result backend (not required for your use case)
CELERY_RESULT_BACKEND = os.getenv(
    "CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

# ----------------------------------------------------
# Create Celery application
# ----------------------------------------------------

celery = Celery(
    "microfarm_etl",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
)

# Load Celery-specific config values
celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

# Autodiscover tasks from tasks.py
celery.autodiscover_tasks(["tasks"])


# ----------------------------------------------------
# Schedule ETL task
# ----------------------------------------------------
celery.conf.beat_schedule = {
    "generate-fake-data-every-minute": {
        "task": "run_etl_task",   # must match task name in tasks.py
        "schedule": 60.0,         # every 60 seconds
        # Example for every hour at minute 0:
        # "schedule": crontab(minute=0)
    },
}
