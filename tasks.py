from celery_app import celery
from app import generate_all_farms

# ----------------------------------------------------
# Celery Task: Run ETL for all farms
# ----------------------------------------------------


@celery.task(name="run_etl_task")
def run_etl_task():
    """
    Celery task that executes the generate_all_farms ETL loop.
    """
    return generate_all_farms()
