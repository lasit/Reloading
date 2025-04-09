import streamlit as st
from typing import Dict, Any, List, Optional
import utils
import datetime
import re
import os

def create_empty_test_data() -> Dict[str, Any]:
    """
    Create an empty test data structure with default values.
    
    Returns:
        Dictionary with default test data structure
    """
    today = datetime.date.today().isoformat()
    
    return {
        "test_id": "",
        "date": today,
        "distance_m": 100,
        
        "platform": {
            "calibre": "",
            "rifle": "",
            "barrel_length_in": 0.0,
            "twist_rate": ""
        },
        
        "ammo": {
            "case": {
                "brand": "",
                "lot": ""
            },
            "bullet": {
                "brand": "",
                "model": "",
                "weight_gr": 0.0,
                "lot": ""
            },
            "powder": {
                "brand": "",
                "model": "",
                "charge_gr": 0.0,
                "lot": ""
            },
            "primer": {
                "brand": "",
                "model": "",
                "lot": ""
            },
            "coal_in": 0.0,
            "b2o_in": 0.0
        },
        
        "environment": {
            "temperature_c": 0.0,
            "humidity_percent": 0,
            "pressure_hpa": 0,
            "wind_speed_mps": 0.0,
            "wind_dir_deg": 0,
            "weather": "Clear"
        },
        
        "group": {
            "group_es_mm": 0.0,
            "group_es_moa": 0.0,
            "group_es_x_mm": 0.0,
            "group_es_y_mm": 0.0,
            "mean_radius_mm": 0.0,
            "poi_x_mm": 0.0,
            "poi_y_mm": 0.0,
            "shots": 5
        },
        
        "chrono": {
            "avg_velocity_fps": 0.0,
            "sd_fps": 0.0,
            "es_fps": 0.0
        },
        
        "files": {
            "chrono_csv": "chrono.csv",
            "target_photo": "target.jpg"
        },
        
        "notes": ""
    }


def calculate_moa(group_size_mm: float, distance_m: float) -> float:
    """
    Calculate MOA (Minute of Angle) from group size and distance.
    
    Args:
        group_size_mm: Group size in millimeters
        distance_m: Distance in meters
        
    Returns:
        Group size in MOA
    """
    # MOA = (group size in inches / distance in yards) * 100
    # 1 inch = 25.4 mm
    # 1 yard = 0.9144 meters
    
    if distance_m <= 0 or group_size_mm <= 0:
        return 0.0
    
    group_size_inches = group_size_mm / 25.4
    distance_yards = distance_m / 0.9144
    
    moa = (group_size_inches / distance_yards) * 100
    
    return round(moa, 2)


def parse_test_id(test_id: str) -> Dict[str, Any]:
    """
    Parse a test ID into its components and return a data dictionary.
    
    Args:
        test_id: Test ID string in the format:
                [Date]__[Distance]_[Calibre]_[Rifle]_[BulletModel]_[BulletWeight]_[Powder]_[Charge]_[COAL]_[Primer]
    
    Returns:
        Dictionary with parsed values
    """
    data = create_empty_test_data()
    data["test_id"] = test_id
    
    try:
        # Split by double underscore first
        date_part, rest = test_id.split('__')
        
        # Split the rest by single underscore
        parts = rest.split('_')
        
        if len(parts) < 10:
            # Not enough parts, return empty data
            return data
        
        # Parse date
        if len(date_part) == 8:  # YYYYMMDD format
            data["date"] = f"{date_part[:4]}-{date_part[4:6]}-{date_part[6:8]}"
        
        # Parse distance
        distance_str = parts[0]
        if distance_str.endswith('m'):
            distance_str = distance_str[:-1]  # Remove 'm' suffix
        try:
            data["distance_m"] = int(distance_str)
        except ValueError:
            pass
        
        # Parse platform
        data["platform"]["calibre"] = parts[1]
        data["platform"]["rifle"] = parts[2]
        
        # Parse bullet
        data["ammo"]["bullet"]["model"] = parts[3]
        bullet_weight_str = parts[4]
        if bullet_weight_str.endswith('gr'):
            bullet_weight_str = bullet_weight_str[:-2]  # Remove 'gr' suffix
        try:
            data["ammo"]["bullet"]["weight_gr"] = float(bullet_weight_str)
        except ValueError:
            pass
        
        # Parse powder
        data["ammo"]["powder"]["model"] = parts[5]
        powder_charge_str = parts[6]
        if powder_charge_str.endswith('gr'):
            powder_charge_str = powder_charge_str[:-2]  # Remove 'gr' suffix
        try:
            data["ammo"]["powder"]["charge_gr"] = float(powder_charge_str)
        except ValueError:
            pass
        
        # Parse COAL
        coal_str = parts[7]
        if coal_str.endswith('in'):
            coal_str = coal_str[:-2]  # Remove 'in' suffix
        try:
            data["ammo"]["coal_in"] = float(coal_str)
        except ValueError:
            pass

        # Parse B2O
        b2o_str = parts[8]
        if b2o_str.endswith('in'):
            b2o_str = b2o_str[:-2]  # Remove 'in' suffix
        try:
            data["ammo"]["b2o_in"] = float(b2o_str)
        except ValueError:
            pass
        
        # Parse primer
        data["ammo"]["primer"]["model"] = parts[9]
        
    except Exception as e:
        print(f"Error parsing test ID: {e}")
    
    return data


def generate_test_id(data: Dict[str, Any]) -> str:
    """
    Generate a test ID from test data.
    
    Args:
        data: Test data dictionary
        
    Returns:
        Formatted test ID string
    """
    # Clean and format inputs
    date_str = data["date"].replace('-', '')
    
    # Replace spaces with hyphens and remove special characters
    def clean_str(s: str) -> str:
        s = re.sub(r'[^\w\s-]', '', str(s))  # Remove special chars except hyphen
        s = re.sub(r'\s+', '-', s)           # Replace spaces with hyphens
        return s
    
    calibre_clean = clean_str(data["platform"]["calibre"])
    rifle_clean = clean_str(data["platform"]["rifle"])
    bullet_model_clean = clean_str(data["ammo"]["bullet"]["model"])
    powder_model_clean = clean_str(data["ammo"]["powder"]["model"])
    primer_model_clean = clean_str(data["ammo"]["primer"]["model"])
    
    # Format the test ID with 3 decimal places for COAL and B2O
    test_id = f"{date_str}__{data['distance_m']}m_{calibre_clean}_{rifle_clean}_{bullet_model_clean}_{data['ammo']['bullet']['weight_gr']}gr_{powder_model_clean}_{data['ammo']['powder']['charge_gr']}gr_{data['ammo']['coal_in']:.3f}in_{data['ammo']['b2o_in']:.3f}in_{primer_model_clean}"
    
    return test_id


def create_test_form(test_data: Dict[str, Any], new_test: bool = False) -> Dict[str, Any]:
    """
    Create a form for editing test data.
    
    Args:
        test_data: Current test data
        new_test: Whether this is a new test
        
    Returns:
        Updated test data and whether the form was submitted
    """
    with st.form("test_data_form"):
        # Create tabs for different sections
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📋 Test Info", 
            "🔫 Platform", 
            "🧪 Ammunition", 
            "🌡️ Environment", 
            "🎯 Results", 
            "📝 Notes"
        ])
        
        # Tab 1: Test Information
        with tab1:
            st.header("Test Information")
            
            col1, col2 = st.columns(2)
            with col1:
                date = st.date_input(
                    "Date", 
                    value=datetime.date.fromisoformat(test_data["date"]) if test_data["date"] else datetime.date.today()
                )
                test_data["date"] = date.isoformat()
            with col2:
                test_data["distance_m"] = st.number_input(
                    "Distance (m)", 
                    min_value=0, 
                    value=int(test_data["distance_m"]),
                    step=25
                )
            
            # Display current test ID
            if test_data["test_id"]:
                st.subheader("Current Test ID")
                st.code(test_data["test_id"])
        
        # Tab 2: Platform
        with tab2:
            st.header("Platform Configuration")
            
            col1, col2 = st.columns(2)
            with col1:
                test_data["platform"]["calibre"] = st.text_input(
                    "Calibre", 
                    value=test_data["platform"]["calibre"],
                    placeholder="e.g. 223_Rem"
                )
                test_data["platform"]["rifle"] = st.text_input(
                    "Rifle", 
                    value=test_data["platform"]["rifle"],
                    placeholder="e.g. Tikka_T3x"
                )
            with col2:
                test_data["platform"]["barrel_length_in"] = st.number_input(
                    "Barrel Length (inches)", 
                    min_value=0.0, 
                    value=float(test_data["platform"]["barrel_length_in"]),
                    step=0.1
                )
                test_data["platform"]["twist_rate"] = st.text_input(
                    "Twist Rate", 
                    value=test_data["platform"]["twist_rate"],
                    placeholder="e.g. 1:8"
                )
        
        # Tab 3: Ammunition
        with tab3:
            st.header("Ammunition Configuration")
            
            # Case
            st.subheader("Case")
            col1, col2 = st.columns(2)
            with col1:
                test_data["ammo"]["case"]["brand"] = st.text_input(
                    "Brand", 
                    value=test_data["ammo"]["case"]["brand"],
                    key="case_brand", 
                    placeholder="e.g. Sako"
                )
            with col2:
                test_data["ammo"]["case"]["lot"] = st.text_input(
                    "Lot", 
                    value=test_data["ammo"]["case"]["lot"],
                    key="case_lot", 
                    placeholder="e.g. SK-001"
                )
            
            # Bullet
            st.subheader("Bullet")
            col1, col2 = st.columns(2)
            with col1:
                test_data["ammo"]["bullet"]["brand"] = st.text_input(
                    "Brand", 
                    value=test_data["ammo"]["bullet"]["brand"],
                    key="bullet_brand", 
                    placeholder="e.g. Hornady"
                )
                test_data["ammo"]["bullet"]["model"] = st.text_input(
                    "Model", 
                    value=test_data["ammo"]["bullet"]["model"],
                    key="bullet_model", 
                    placeholder="e.g. ELD-M"
                )
            with col2:
                test_data["ammo"]["bullet"]["weight_gr"] = st.number_input(
                    "Weight (gr)", 
                    min_value=0.0, 
                    value=float(test_data["ammo"]["bullet"]["weight_gr"]),
                    key="bullet_weight", 
                    step=0.1
                )
                test_data["ammo"]["bullet"]["lot"] = st.text_input(
                    "Lot", 
                    value=test_data["ammo"]["bullet"]["lot"],
                    key="bullet_lot", 
                    placeholder="e.g. HD2204A"
                )
            
            # Powder
            st.subheader("Powder")
            col1, col2 = st.columns(2)
            with col1:
                test_data["ammo"]["powder"]["brand"] = st.text_input(
                    "Brand", 
                    value=test_data["ammo"]["powder"]["brand"],
                    key="powder_brand", 
                    placeholder="e.g. ADI"
                )
                test_data["ammo"]["powder"]["model"] = st.text_input(
                    "Model", 
                    value=test_data["ammo"]["powder"]["model"],
                    key="powder_model", 
                    placeholder="e.g. 2208"
                )
            with col2:
                test_data["ammo"]["powder"]["charge_gr"] = st.number_input(
                    "Charge (gr)", 
                    min_value=0.0, 
                    value=float(test_data["ammo"]["powder"]["charge_gr"]),
                    key="powder_charge", 
                    step=0.1
                )
                test_data["ammo"]["powder"]["lot"] = st.text_input(
                    "Lot", 
                    value=test_data["ammo"]["powder"]["lot"],
                    key="powder_lot", 
                    placeholder="e.g. ADI-2208-03"
                )
            
            # Primer
            st.subheader("Primer")
            col1, col2 = st.columns(2)
            with col1:
                test_data["ammo"]["primer"]["brand"] = st.text_input(
                    "Brand", 
                    value=test_data["ammo"]["primer"]["brand"],
                    key="primer_brand", 
                    placeholder="e.g. CCI"
                )
                test_data["ammo"]["primer"]["model"] = st.text_input(
                    "Model", 
                    value=test_data["ammo"]["primer"]["model"],
                    key="primer_model", 
                    placeholder="e.g. BR4"
                )
            with col2:
                test_data["ammo"]["primer"]["lot"] = st.text_input(
                    "Lot", 
                    value=test_data["ammo"]["primer"]["lot"],
                    key="primer_lot", 
                    placeholder="e.g. CCI-BR4-B1"
                )
            
            # Cartridge Measurements
            st.subheader("Cartridge Measurements")
            test_data["ammo"]["coal_in"] = st.number_input(
                "Cartridge Overall Length - COAL (inches)", 
                min_value=0.0, 
                value=float(test_data["ammo"]["coal_in"]),
                step=0.001
            )
            test_data["ammo"]["b2o_in"] = st.number_input(
                "Cartridge Base to Ogive - B2O (inches)",
                min_value=0.0,
                value=float(test_data["ammo"]["b2o_in"]),
                step=0.001
            )
        
        # Tab 4: Environment
        with tab4:
            st.header("Environmental Conditions")
            
            col1, col2 = st.columns(2)
            with col1:
                test_data["environment"]["temperature_c"] = st.number_input(
                    "Temperature (°C)", 
                    value=float(test_data["environment"]["temperature_c"]),
                    step=0.1
                )
                test_data["environment"]["humidity_percent"] = st.number_input(
                    "Humidity (%)", 
                    min_value=0, 
                    max_value=100, 
                    value=int(test_data["environment"]["humidity_percent"]),
                    step=1
                )
                test_data["environment"]["pressure_hpa"] = st.number_input(
                    "Pressure (hPa)", 
                    min_value=0, 
                    value=int(test_data["environment"]["pressure_hpa"]),
                    step=1
                )
            with col2:
                test_data["environment"]["wind_speed_mps"] = st.number_input(
                    "Wind Speed (m/s)", 
                    min_value=0.0, 
                    value=float(test_data["environment"]["wind_speed_mps"]),
                    step=0.1
                )
                test_data["environment"]["wind_dir_deg"] = st.number_input(
                    "Wind Direction (degrees)", 
                    min_value=0, 
                    max_value=360, 
                    value=int(test_data["environment"]["wind_dir_deg"]),
                    step=1
                )
                test_data["environment"]["weather"] = st.selectbox(
                    "Weather Conditions", 
                    options=["Clear", "Overcast", "Rain", "Fog", "Variable"],
                    index=["Clear", "Overcast", "Rain", "Fog", "Variable"].index(test_data["environment"]["weather"]) if test_data["environment"]["weather"] in ["Clear", "Overcast", "Rain", "Fog", "Variable"] else 0
                )
        
        # Tab 5: Results
        with tab5:
            st.header("Group Measurements")
            
            col1, col2 = st.columns(2)
            with col1:
                group_es_mm = st.number_input(
                    "Group Extreme Spread (mm)", 
                    min_value=0.0, 
                    value=float(test_data["group"]["group_es_mm"]),
                    step=0.1
                )
                test_data["group"]["group_es_mm"] = group_es_mm
                
                # Auto-calculate MOA
                if group_es_mm > 0 and test_data["distance_m"] > 0:
                    test_data["group"]["group_es_moa"] = calculate_moa(group_es_mm, test_data["distance_m"])
                
                st.number_input(
                    "Group Extreme Spread (MOA)", 
                    min_value=0.0, 
                    value=float(test_data["group"]["group_es_moa"]),
                    step=0.01,
                    disabled=True
                )
                
                test_data["group"]["group_es_x_mm"] = st.number_input(
                    "Group Extreme Spread X (mm)", 
                    min_value=0.0, 
                    value=float(test_data["group"]["group_es_x_mm"]),
                    step=0.1
                )
            with col2:
                test_data["group"]["group_es_y_mm"] = st.number_input(
                    "Group Extreme Spread Y (mm)", 
                    min_value=0.0, 
                    value=float(test_data["group"]["group_es_y_mm"]),
                    step=0.1
                )
                test_data["group"]["mean_radius_mm"] = st.number_input(
                    "Mean Radius (mm)", 
                    min_value=0.0, 
                    value=float(test_data["group"]["mean_radius_mm"]),
                    step=0.1
                )
                test_data["group"]["shots"] = st.number_input(
                    "Number of Shots", 
                    min_value=1, 
                    value=int(test_data["group"]["shots"]),
                    step=1
                )
            
            col1, col2 = st.columns(2)
            with col1:
                test_data["group"]["poi_x_mm"] = st.number_input(
                    "Point of Impact X (mm)", 
                    value=float(test_data["group"]["poi_x_mm"]),
                    step=0.1
                )
            with col2:
                test_data["group"]["poi_y_mm"] = st.number_input(
                    "Point of Impact Y (mm)", 
                    value=float(test_data["group"]["poi_y_mm"]),
                    step=0.1
                )
            
            st.header("Chronograph Data")
            col1, col2 = st.columns(2)
            with col1:
                test_data["chrono"]["avg_velocity_fps"] = st.number_input(
                    "Average Velocity (fps)", 
                    min_value=0.0, 
                    value=float(test_data["chrono"]["avg_velocity_fps"]),
                    step=0.1
                )
                test_data["chrono"]["sd_fps"] = st.number_input(
                    "Standard Deviation (fps)", 
                    min_value=0.0, 
                    value=float(test_data["chrono"]["sd_fps"]),
                    step=0.1
                )
            with col2:
                test_data["chrono"]["es_fps"] = st.number_input(
                    "Extreme Spread (fps)", 
                    min_value=0.0, 
                    value=float(test_data["chrono"]["es_fps"]),
                    step=0.1
                )
        
        # Tab 6: Notes and Files
        with tab6:
            st.header("Files")
            col1, col2 = st.columns(2)
            with col1:
                test_data["files"]["chrono_csv"] = st.text_input(
                    "Chronograph CSV", 
                    value=test_data["files"]["chrono_csv"],
                    placeholder="e.g. chrono.csv"
                )
            with col2:
                test_data["files"]["target_photo"] = st.text_input(
                    "Target Photo", 
                    value=test_data["files"]["target_photo"],
                    placeholder="e.g. target.jpg"
                )
            
            st.header("Notes")
            test_data["notes"] = st.text_area(
                "Additional Notes", 
                value=test_data["notes"],
                height=200
            )
        
        # Submit button
        submitted = st.form_submit_button("Save Test Data")
        
        if submitted:
            if not test_data["test_id"]:
                st.error("Test ID is required. Please select an existing test or generate a new test ID.")
                return test_data, False
            
            # Save the data
            utils.save_test_data(test_data["test_id"], test_data)
            
            # Check if files exist
            test_folder = os.path.join("tests", test_data["test_id"])
            if test_data["files"]["chrono_csv"] and not os.path.exists(os.path.join(test_folder, test_data["files"]["chrono_csv"])):
                st.warning(f"Note: Chronograph CSV file '{test_data['files']['chrono_csv']}' not found in test folder.")
            if test_data["files"]["target_photo"] and not os.path.exists(os.path.join(test_folder, test_data["files"]["target_photo"])):
                st.warning(f"Note: Target photo '{test_data['files']['target_photo']}' not found in test folder.")
            
            return test_data, True
        
        return test_data, False
