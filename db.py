import oracledb
import os

USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASS")
DSN = os.getenv("DB_DSN")
WALLET_PATH = os.getenv("TNS_ADMIN", "/tmp/wallet")  # Render wallet path


def get_connection():
    return oracledb.connect(
        user=USER,
        password=PASSWORD,
        dsn=DSN,
        config_dir=WALLET_PATH
    )


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
        print("INSERT SUCCESS:", data)
    except Exception as e:
        print("INSERT ERROR:", e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
