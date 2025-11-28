import oracledb
import os
from dotenv import load_dotenv

load_dotenv()

WALLET_PATH = os.getenv("WALLET_LOCATION")
USER = os.getenv("DB_USERNAME")
PASSWORD = os.getenv("DB_PASSWORD")
DSN = os.getenv("DSN")


def get_connection():
    return oracledb.connect(
        user=USER,
        password=PASSWORD,
        dsn=DSN,
        config_dir=WALLET_PATH,
        wallet_location=WALLET_PATH
    )


def insert_sensor_data(data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO microfarm_sensors 
        (farm_id, timestamp, soil_moisture, temperature, light_intensity, water_consumed, nutrient_level, plant_growth_stage)
        VALUES (:farm_id, :timestamp, :soil_moisture, :temperature, :light_intensity, :water_consumed, :nutrient_level, :plant_growth_stage)
    """, data)
    conn.commit()
    cursor.close()
    conn.close()
