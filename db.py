import os
import psycopg2
import logging

# ----------------------------
# Logging setup
# ----------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ----------------------------
# Environment variables
# ----------------------------
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_DSN = os.getenv("DB_DSN")

logger.info("=== Oracle DB Debug Info ===")
logger.info(f"DB_USER: {DB_USER}")
logger.info(f"DB_DSN: {DB_DSN}")
logger.info("============================")

# ----------------------------
# DB Connection
# ----------------------------


def get_connection():
    try:
        logger.info("Connecting to Oracle...")
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT', 5432),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            sslmode='require'
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
            VALUES (:farm_id, :timestamp, :soil_moisture, :temperature, :light_intensity, :water_consumed, :nutrient_level, :plant_growth_stage)
        """, data)
        conn.commit()
        logger.info("INSERT SUCCESS: %s", data)
    except Exception as e:
        logger.error("INSERT ERROR: %s", e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
