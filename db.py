import os
import psycopg2
import logging
from psycopg2.extras import RealDictCursor

# ----------------------------
# Logging setup
# ----------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ----------------------------
# Environment variables
# ----------------------------
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

logger.info("=== Postgres DB Debug Info ===")
logger.info(f"DB_HOST: {DB_HOST}")
logger.info(f"DB_PORT: {DB_PORT}")
logger.info(f"DB_NAME: {DB_NAME}")
logger.info(f"DB_USER: {DB_USER}")
logger.info("=============================")

# ----------------------------
# DB Connection
# ----------------------------


def get_connection():
    try:
        logger.info("Connecting to Supabase Postgres...")

        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            sslmode="require"
        )

        logger.info("Connected successfully!")
        return conn

    except Exception as e:
        logger.error("CONNECTION ERROR: %s", e)
        raise

# ----------------------------
# Insert data
# ----------------------------


def insert_sensor_data(data):
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO microfarm_sensors 
            (farm_id, timestamp, soil_moisture, temperature, light_intensity, water_consumed, nutrient_level, plant_growth_stage)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            data["farm_id"],
            data["timestamp"],
            data["soil_moisture"],
            data["temperature"],
            data["light_intensity"],
            data["water_consumed"],
            data["nutrient_level"],
            data["plant_growth_stage"]
        ))

        conn.commit()
        logger.info("INSERT SUCCESS: %s", data)

    except Exception as e:
        logger.error("INSERT ERROR: %s", e)

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
