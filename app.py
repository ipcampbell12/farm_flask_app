from flask import Flask, jsonify
from data_generator import generate_sensor_data
from db import insert_sensor_data

app = Flask(__name__)
NUM_FARMS = 5


@app.route("/")
def index():
    return jsonify({"ok": True, "message": "Flask + Supabase is live!"})


@app.route("/generate")
def generate():
    inserted = []
    for farm_id in range(1, NUM_FARMS+1):
        data = generate_sensor_data(farm_id)
        print("Generated data:", data)
        insert_sensor_data(data)
        inserted.append(data)
    return jsonify(inserted)


if __name__ == "__main__":
    app.run(debug=True)
