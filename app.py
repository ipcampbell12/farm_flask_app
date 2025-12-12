from flask import Flask, jsonify
from data_generator import generate_sensor_data
from db import insert_sensor_data
import os
import logging

# ----------------------------
# App setup
# ----------------------------
app = Flask(__name__)
NUM_FARMS = 5

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ----------------------------
# Health check route
# ----------------------------


@app.route("/")
def index():
    return jsonify({
        "ok": True,
        "message": "Flask + Supabase is live!"
    })

# ----------------------------
# Core ETL logic (NOW reusable)
# ----------------------------


def generate_all_farms(num_farms=NUM_FARMS):
    """Generate and insert data for all farms."""
    inserted = []

    for farm_id in range(1, num_farms + 1):
        try:
            data = generate_sensor_data(farm_id)
            logger.info("Generated data: %s", data)

            insert_sensor_data(data)
            inserted.append(data)

        except Exception as e:
            logger.error("FAILED for farm_id=%s: %s", farm_id, e)

    return inserted

# ----------------------------
# Manual trigger route
# ----------------------------


@app.route("/generate")
def generate():
    """Manually trigger the ETL loop via HTTP."""
    inserted = generate_all_farms()
    return jsonify(inserted)

# ----------------------------
# Local vs Render startup
# ----------------------------


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=True
    )
