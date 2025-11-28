import os
import oracledb

# ----------------------------
# Environment variables
# ----------------------------
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
DSN = os.getenv("DB_DSN")

# ----------------------------
# Debug prints
# ----------------------------
print("=== Oracle DB Debug Info ===")
print("DB_USER:", USER)
print("DB_DSN:", DSN)
print("============================")

# ----------------------------
# DB Connection
# ----------------------------


def get_connection():
    try:
        print("Connecting to Oracle...")
        conn = oracledb.connect(
            user=USER,
            password=PASSWORD,
            dsn=DSN
        )
        print("Connected successfully!")
        return conn
    except Exception as e:
        print("CONNECTION ERROR:", e)
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
        print("INSERT SUCCESS:", data)
    except Exception as e:
        print("INSERT ERROR:", e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
