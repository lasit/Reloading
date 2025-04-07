import os
import yaml
import random
import datetime
import utils
from typing import Dict, Any

# Load component lists
def load_component_lists():
    with open('Component_List.yaml', 'r') as file:
        return yaml.safe_load(file)

# Generate a random date in 2025
def random_date_in_2025():
    start_date = datetime.date(2025, 1, 1)
    end_date = datetime.date(2025, 12, 31)
    days_between = (end_date - start_date).days
    random_days = random.randint(0, days_between)
    return (start_date + datetime.timedelta(days=random_days)).isoformat()

# Generate random test data
def generate_random_test_data(component_lists):
    # Random values for test info
    date = random_date_in_2025()
    distance_m = random.randint(100, 900)
    
    # Random values for platform
    calibre = random.choice(component_lists['calibre'])
    rifle = random.choice(component_lists['rifle'])
    barrel_length_in = round(random.uniform(18, 28), 1)
    twist_rates = ["1:8", "1:10", "1:12", "1:14"]
    twist_rate = random.choice(twist_rates)
    
    # Random values for ammunition - case
    case_brand = random.choice(component_lists['case_brand'])
    case_lot = f"LOT-{random.randint(1, 100)}"
    brass_sizing = random.choice(component_lists['brass_sizing'])
    neck_turned = random.choice(["Yes", "No"])
    shoulder_bump = 1.5  # Fixed value as specified
    bushing_size = 0.245  # Fixed value as specified
    
    # Random values for ammunition - bullet
    bullet_brand = random.choice(component_lists['bullet_brand'])
    bullet_model = random.choice(component_lists['bullet_model'])
    bullet_lot = f"LOT-{random.randint(1, 100)}"
    bullet_weight = 75  # Fixed value as specified (75 or 75)
    
    # Random values for ammunition - powder
    powder_brand = random.choice(component_lists['powder_brand'])
    powder_model = random.choice(component_lists['powder_model'])
    powder_lot = f"LOT-{random.randint(1, 100)}"
    powder_charge = round(random.uniform(23.2, 24.1), 1)
    
    # Random values for ammunition - primer
    primer_brand = random.choice(component_lists['primer_brand'])
    primer_model = random.choice(component_lists['primer_model'])
    primer_lot = f"LOT-{random.randint(1, 100)}"
    
    # Fixed values for cartridge measurements
    coal_in = 2.412
    b2o_in = 1.783
    
    # Random values for environmental conditions
    temperature_c = random.choice([30, 32, 34, 36])
    wind_speed_mps = random.choice([0, 2, 4, 6])
    humidity_percent = random.choice([40, 60, 80])
    wind_dir_deg = random.choice([0, 30, 60, 90])
    pressure_hpa = random.choice([1008, 1009, 1010])
    weather_conditions = random.choice(["Clear", "Overcast", "Rain", "Fog", "Variable"])
    
    # Random values for group measurements
    shots = random.choice([8, 10, 12, 14, 16])
    group_es_mm = round(random.uniform(10, 200), 1)
    group_es_moa = round(random.uniform(0.1, 2), 2)
    group_es_x_mm = round(random.uniform(10, 200), 1)
    group_es_y_mm = round(random.uniform(10, 200), 1)
    mean_radius_mm = round(random.uniform(10, 50), 1)
    poi_x_mm = round(random.uniform(10, 200), 1)
    poi_y_mm = round(random.uniform(10, 200), 1)
    
    # Random values for chronograph data
    avg_velocity_fps = round(random.uniform(1600, 1900), 1)
    es_fps = round(random.uniform(10, 100), 1)
    sd_fps = round(random.uniform(5, 30), 1)
    
    # Random notes about weather
    weather_notes = [
        "The weather was clear with a slight breeze from the east.",
        "Overcast conditions with occasional gusts of wind.",
        "Perfect shooting conditions with clear skies and minimal wind.",
        "High humidity made for challenging shooting conditions.",
        "Light rain started during the test but did not significantly impact results.",
        "Strong winds from the north affected shot placement.",
        "Excellent visibility with stable atmospheric conditions.",
        "Changing wind directions throughout the test session.",
        "Hot and humid conditions with mirage affecting sight picture.",
        "Cool morning with stable air and good visibility."
    ]
    notes = random.choice(weather_notes) + " " + random.choice(weather_notes)
    
    # Create test data structure
    test_data = {
        "test_id": "",  # Will be generated later
        "date": date,
        "distance_m": distance_m,
        
        "platform": {
            "calibre": calibre,
            "rifle": rifle,
            "barrel_length_in": barrel_length_in,
            "twist_rate": twist_rate
        },
        
        "ammo": {
            "case": {
                "brand": case_brand,
                "lot": case_lot,
                "neck_turned": neck_turned,
                "brass_sizing": brass_sizing,
                "bushing_size": bushing_size,
                "shoulder_bump": shoulder_bump
            },
            "bullet": {
                "brand": bullet_brand,
                "model": bullet_model,
                "weight_gr": bullet_weight,
                "lot": bullet_lot
            },
            "powder": {
                "brand": powder_brand,
                "model": powder_model,
                "charge_gr": powder_charge,
                "lot": powder_lot
            },
            "primer": {
                "brand": primer_brand,
                "model": primer_model,
                "lot": primer_lot
            },
            "coal_in": coal_in,
            "b2o_in": b2o_in
        },
        
        "environment": {
            "temperature_c": temperature_c,
            "humidity_percent": humidity_percent,
            "pressure_hpa": pressure_hpa,
            "wind_speed_mps": wind_speed_mps,
            "wind_dir_deg": wind_dir_deg,
            "weather": weather_conditions
        },
        
        "group": {
            "group_es_mm": group_es_mm,
            "group_es_moa": group_es_moa,
            "group_es_x_mm": group_es_x_mm,
            "group_es_y_mm": group_es_y_mm,
            "mean_radius_mm": mean_radius_mm,
            "poi_x_mm": poi_x_mm,
            "poi_y_mm": poi_y_mm,
            "shots": shots
        },
        
        "chrono": {
            "avg_velocity_fps": avg_velocity_fps,
            "sd_fps": sd_fps,
            "es_fps": es_fps
        },
        
        "files": {
            "chrono_csv": "chrono.csv",
            "target_photo": "target.jpg"
        },
        
        "notes": notes
    }
    
    # Generate test ID
    test_id = generate_test_id(
        date,
        distance_m,
        calibre,
        rifle,
        case_brand,
        bullet_brand,
        bullet_model,
        bullet_weight,
        powder_brand,
        powder_model,
        powder_charge,
        coal_in,
        b2o_in,
        primer_brand,
        primer_model
    )
    
    test_data["test_id"] = test_id
    
    return test_data

# Generate test ID (copied from app.py)
def generate_test_id(date: str, distance_m: int, calibre: str, rifle: str, 
                    case_brand: str, bullet_brand: str, bullet_model: str, bullet_weight: float, 
                    powder_brand: str, powder_model: str, powder_charge: float, 
                    coal: float, b2o: float, primer_brand: str, primer_model: str) -> str:
    """
    Generate a test ID from components.
    """
    import re
    
    # Keep the date format with hyphens (original format)
    date_str = date
    
    # Replace spaces with hyphens and remove special characters
    def clean_str(s: str) -> str:
        s = re.sub(r'[^\w\s-]', '', s)  # Remove special chars except hyphen
        s = re.sub(r'\s+', '-', s)      # Replace spaces with hyphens
        return s
    
    calibre_clean = clean_str(calibre)
    rifle_clean = clean_str(rifle)
    case_brand_clean = clean_str(case_brand)
    bullet_brand_clean = clean_str(bullet_brand)
    bullet_model_clean = clean_str(bullet_model)
    powder_brand_clean = clean_str(powder_brand)
    powder_model_clean = clean_str(powder_model)
    primer_brand_clean = clean_str(primer_brand)
    primer_model_clean = clean_str(primer_model)
    
    # Format the test ID with the original format
    # Use integer values for weights (no decimal points) and format COAL with 3 decimal places
    test_id = f"{date_str}__{distance_m}m_{calibre_clean}_{rifle_clean}_{case_brand_clean}_{bullet_brand_clean}_{bullet_model_clean}_{int(bullet_weight)}gr_{powder_brand_clean}_{powder_model_clean}_{int(powder_charge)}gr_{coal:.3f}in_{b2o:.3f}in_{primer_brand_clean}_{primer_model_clean}"
    
    return test_id

# Main function to generate and save test data
def main():
    component_lists = load_component_lists()
    
    # Create 50 random test data files
    for i in range(50):
        test_data = generate_random_test_data(component_lists)
        test_id = test_data["test_id"]
        
        # Save the test data
        utils.save_test_data(test_id, test_data)
        print(f"Generated test data for '{test_id}'")

if __name__ == "__main__":
    main()
