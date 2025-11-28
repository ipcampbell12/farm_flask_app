import random
from datetime import datetime

def generate_sensor_data(farm_id):
    return {
        "farm_id": farm_id,
        "timestamp": datetime.now(),
        "soil_moisture": round(random.uniform(20, 80), 2),
        "temperature": round(random.uniform(15, 35), 2),
        "light_intensity": round(random.uniform(100, 1000), 2),
        "water_consumed": round(random.uniform(0.5, 5), 2),
        "nutrient_level": round(random.uniform(40, 100), 2),
        "plant_growth_stage": random.choice(["seedling","vegetative","flowering","harvestable"])
    }
