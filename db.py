import os
import oracledb

# ----------------------------
# Environment variables
# ----------------------------
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASS")
DSN = os.getenv("DB_DSN")
WALLET_PATH = os.getenv("TNS_ADMIN", "/tmp/wallet")  # Render wallet path

# Ensure Oracle client sees the wallet
os.environ["TNS_ADMIN"] = WALLET_PATH

# ----------------------------
# Debug prints
# ----------------------------
print("=== Oracle DB Debug Info ===")
print("DB_USER:", USER)
print("DB_DSN:", DSN)
print("Wallet path (TNS_ADMIN):", WALLET_PATH)
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
            dsn=DSN,
            config_dir=WALLET_PATH
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
