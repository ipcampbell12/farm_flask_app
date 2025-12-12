from celery_app import celery

# --------------------------------------------
# Celery Worker Entrypoint
# --------------------------------------------

if __name__ == "__main__":
    """
    This starts the Celery worker process.

    Equivalent to running:
        celery -A celery_app worker --loglevel=info
    """
    celery.worker_main([
        "worker",
        "--loglevel=info"
    ])
