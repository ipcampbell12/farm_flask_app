from data_generator import generate_sensor_data
from db import insert_sensor_data
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

NUM_FARMS = 5


def main():
    logger.info("CRON JOB STARTED")

    for farm_id in range(1, NUM_FARMS + 1):
        try:
            data = generate_sensor_data(farm_id)
            insert_sensor_data(data)
            logger.info("Inserted: %s", data)
        except Exception as e:
            logger.error("FAILED for farm %s: %s", farm_id, e)

    logger.info("CRON JOB COMPLETED")


if __name__ == "__main__":
    main()
