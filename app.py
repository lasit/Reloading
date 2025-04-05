import streamlit as st
import datetime
import os
import re
from typing import Dict, Any, Optional, Tuple
import utils

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
            "coal_in": 0.0
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


def parse_test_id(test_id: str) -> Tuple[str, str, str, str, str, str, str, str, str, str, str, str, str, str]:
    """
    Parse a test ID into its components.
    
    Args:
        test_id: Test ID string in the format:
                [Date]__[Distance]_[Calibre]_[Rifle]_[CaseBrand]_[BulletBrand]_[BulletModel]_[BulletWeight]_[PowderBrand]_[Powder]_[Charge]_[COAL]_[PrimerBrand]_[Primer]
    
    Returns:
        Tuple of (date, distance, calibre, rifle, case_brand, bullet_brand, bullet_model, bullet_weight, powder_brand, powder_model, charge, coal, primer_brand, primer_model)
    """
    try:
        # Split by double underscore first
        parts = test_id.split('__')
        if len(parts) != 2:
            return ("", "", "", "", "", "", "", "", "", "", "", "", "", "")
        
        date_part = parts[0]
        rest = parts[1]
        
        # Split the rest by single underscore
        parts = rest.split('_')
        
        # Check if we have enough parts for the new format
        if len(parts) >= 13:
            # New format with all brand fields
            distance = parts[0]
            calibre = parts[1]
            rifle = parts[2]
            case_brand = parts[3]
            bullet_brand = parts[4]
            bullet_model = parts[5]
            bullet_weight = parts[6]
            powder_brand = parts[7]
            powder_model = parts[8]
            charge = parts[9]
            coal = parts[10]
            primer_brand = parts[11]
            primer_model = parts[12]
            
            return (date_part, distance, calibre, rifle, case_brand, bullet_brand, bullet_model, bullet_weight, powder_brand, powder_model, charge, coal, primer_brand, primer_model)
        else:
            # Old format without brand fields
            # This is for backward compatibility
            if len(parts) < 9:
                # Not enough parts, return empty values
                return ("", "", "", "", "", "", "", "", "", "", "", "", "", "")
            
            distance = parts[0]
            calibre = parts[1]
            rifle = parts[2]
            bullet_model = parts[3]
            bullet_weight = parts[4]
            powder_model = parts[5]
            charge = parts[6]
            coal = parts[7]
            primer_model = parts[8]
            
            # Fill in empty values for the new fields
            case_brand = ""
            bullet_brand = ""
            powder_brand = ""
            primer_brand = ""
            
            return (date_part, distance, calibre, rifle, case_brand, bullet_brand, bullet_model, bullet_weight, powder_brand, powder_model, charge, coal, primer_brand, primer_model)
    except Exception as e:
        print(f"Error parsing test ID: {e}")
        # If parsing fails, return empty values
        return ("", "", "", "", "", "", "", "", "", "", "", "", "", "")


def generate_test_id(date: str, distance_m: int, calibre: str, rifle: str, 
                    case_brand: str, bullet_brand: str, bullet_model: str, bullet_weight: float, 
                    powder_brand: str, powder_model: str, powder_charge: float, 
                    coal: float, primer_brand: str, primer_model: str) -> str:
    """
    Generate a test ID from components.
    
    Args:
        Various test parameters
    
    Returns:
        Formatted test ID string
    """
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
    test_id = f"{date_str}__{distance_m}m_{calibre_clean}_{rifle_clean}_{case_brand_clean}_{bullet_brand_clean}_{bullet_model_clean}_{int(bullet_weight)}gr_{powder_brand_clean}_{powder_model_clean}_{int(powder_charge)}gr_{coal:.3f}in_{primer_brand_clean}_{primer_model_clean}"
    
    return test_id


def load_test_data(test_id: str) -> Dict[str, Any]:
    """
    Load test data for a specific test ID.
    
    Args:
        test_id: Test ID to load
    
    Returns:
        Dictionary containing the test data
    """
    if not test_id:
        return create_empty_test_data()
    
    data = utils.get_test_data(test_id)
    
    # If no data was found, create empty data
    if not data:
        data = create_empty_test_data()
        data["test_id"] = test_id
        
        # Try to parse test ID to pre-fill some fields
        date_str, distance_str, calibre, rifle, case_brand, bullet_brand, bullet_model, bullet_weight_str, powder_brand, powder_model, powder_charge_str, coal_str, primer_brand, primer_model = parse_test_id(test_id)
        
        if date_str:
            try:
                # Format date as YYYY-MM-DD
                if len(date_str) == 8:  # YYYYMMDD format
                    data["date"] = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
            except:
                pass
                
        if distance_str:
            try:
                # Remove 'm' suffix if present
                distance_str = distance_str.rstrip('m')
                data["distance_m"] = int(distance_str)
            except:
                pass
                
        # Platform
        data["platform"]["calibre"] = calibre
        data["platform"]["rifle"] = rifle
        
        # Case
        data["ammo"]["case"]["brand"] = case_brand
        
        # Bullet
        data["ammo"]["bullet"]["brand"] = bullet_brand
        data["ammo"]["bullet"]["model"] = bullet_model
        try:
            # Remove 'gr' suffix if present
            bullet_weight_str = bullet_weight_str.rstrip('gr')
            data["ammo"]["bullet"]["weight_gr"] = float(bullet_weight_str)
        except:
            pass
            
        # Powder
        data["ammo"]["powder"]["brand"] = powder_brand
        data["ammo"]["powder"]["model"] = powder_model
        try:
            # Remove 'gr' suffix if present
            powder_charge_str = powder_charge_str.rstrip('gr')
            data["ammo"]["powder"]["charge_gr"] = float(powder_charge_str)
        except:
            pass
            
        # COAL
        try:
            # Remove 'in' suffix if present
            coal_str = coal_str.rstrip('in')
            data["ammo"]["coal_in"] = float(coal_str)
        except:
            pass
            
        # Primer
        data["ammo"]["primer"]["brand"] = primer_brand
        data["ammo"]["primer"]["model"] = primer_model
    
    return data


def main():
    st.set_page_config(
        page_title="Precision Load Development",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    
    st.title("Precision Rifle Load Development")
    st.markdown("---")
    
    # Sidebar for test selection
    with st.sidebar:
        st.header("Test Selection")
        
        # Get list of test folders
        test_folders = utils.get_test_folders()
        
        # Add search box for filtering tests
        search_query = st.text_input("Search Tests", key="search_tests", placeholder="Filter by test ID...")
        
        # Filter test folders based on search query
        if search_query:
            filtered_test_folders = [folder for folder in test_folders if search_query.lower() in folder.lower()]
        else:
            filtered_test_folders = test_folders
        
        # Option to create a new test
        new_test = st.checkbox("Create new test", key="new_test_checkbox")
        
        if new_test:
            st.info("Fill in the form and click 'Generate Test ID' to create a new test.")
            test_id = ""
        else:
            if filtered_test_folders:
                test_id = st.selectbox(
                    "Select existing test",
                    options=filtered_test_folders,
                    index=0 if filtered_test_folders else None,
                    format_func=lambda x: x.split('__')[1] if '__' in x else x,
                    key="existing_test_id"
                )
                
                # Display number of filtered tests
                if search_query and len(filtered_test_folders) < len(test_folders):
                    st.caption(f"Showing {len(filtered_test_folders)} of {len(test_folders)} tests")
            else:
                if search_query:
                    st.warning(f"No tests found matching '{search_query}'. Clear search or create a new test.")
                    test_id = ""
                else:
                    st.warning("No existing tests found. Create a new test instead.")
                    test_id = ""
                    new_test = True
    
    # Load test data
    test_data = load_test_data(test_id)
    
    # Handle test ID generation outside the form
    if new_test:
        st.subheader("Generate Test ID")
        st.info("Fill in the required fields below and click 'Generate Test ID' to create a new test folder.")
        
        # Create a mini-form for test ID generation
        col1, col2 = st.columns(2)
        with col1:
            gen_date = st.date_input(
                "Date *", 
                value=datetime.date.fromisoformat(test_data["date"]) if test_data["date"] else datetime.date.today(),
                key="gen_date"
            )
        with col2:
            gen_distance_m = st.number_input(
                "Distance (m) *", 
                min_value=0, 
                value=int(test_data["distance_m"]),
                step=25,
                key="gen_distance"
            )
        
        col1, col2 = st.columns(2)
        with col1:
            gen_calibre = st.text_input(
                "Calibre *", 
                value=test_data["platform"]["calibre"],
                placeholder="e.g. 223_Rem",
                key="gen_calibre"
            )
            gen_rifle = st.text_input(
                "Rifle *", 
                value=test_data["platform"]["rifle"],
                placeholder="e.g. Tikka_T3x",
                key="gen_rifle"
            )
            gen_case_brand = st.text_input(
                "Case Brand *", 
                value=test_data["ammo"]["case"]["brand"],
                placeholder="e.g. Lapua",
                key="gen_case_brand"
            )
        with col2:
            gen_bullet_brand = st.text_input(
                "Bullet Brand *", 
                value=test_data["ammo"]["bullet"]["brand"],
                placeholder="e.g. Hornady",
                key="gen_bullet_brand"
            )
            gen_bullet_model = st.text_input(
                "Bullet Model *", 
                value=test_data["ammo"]["bullet"]["model"],
                placeholder="e.g. ELD-M",
                key="gen_bullet_model"
            )
            gen_bullet_weight = st.number_input(
                "Bullet Weight (gr) *", 
                min_value=0.0, 
                value=float(test_data["ammo"]["bullet"]["weight_gr"]),
                step=0.1,
                key="gen_bullet_weight"
            )
        
        col1, col2 = st.columns(2)
        with col1:
            gen_powder_brand = st.text_input(
                "Powder Brand *", 
                value=test_data["ammo"]["powder"]["brand"],
                placeholder="e.g. ADI",
                key="gen_powder_brand"
            )
            gen_powder_model = st.text_input(
                "Powder Model *", 
                value=test_data["ammo"]["powder"]["model"],
                placeholder="e.g. 2208",
                key="gen_powder_model"
            )
            gen_powder_charge = st.number_input(
                "Powder Charge (gr) *", 
                min_value=0.0, 
                value=float(test_data["ammo"]["powder"]["charge_gr"]),
                step=0.1,
                key="gen_powder_charge"
            )
        with col2:
            gen_coal = st.number_input(
                "COAL (inches) *", 
                min_value=0.0, 
                value=float(test_data["ammo"]["coal_in"]),
                step=0.001,
                key="gen_coal"
            )
            gen_primer_brand = st.text_input(
                "Primer Brand *", 
                value=test_data["ammo"]["primer"]["brand"],
                placeholder="e.g. CCI",
                key="gen_primer_brand"
            )
            gen_primer_model = st.text_input(
                "Primer Model *", 
                value=test_data["ammo"]["primer"]["model"],
                placeholder="e.g. BR4",
                key="gen_primer_model"
            )
        
        # Check if all required fields are filled
        all_fields_filled = (
            gen_calibre and 
            gen_rifle and 
            gen_case_brand and 
            gen_bullet_brand and 
            gen_bullet_model and 
            gen_bullet_weight > 0 and 
            gen_powder_brand and 
            gen_powder_model and 
            gen_powder_charge > 0 and 
            gen_coal > 0 and 
            gen_primer_brand and 
            gen_primer_model
        )
        
        # Display a message if fields are missing
        if not all_fields_filled:
            st.warning("All fields marked with * are required. Please fill in all fields to enable the Generate Test ID button.")
        
        # Disable the button if not all fields are filled
        generate_id = st.button("Generate Test ID", disabled=not all_fields_filled)
        
        if generate_id and all_fields_filled:
            # Get values from form
            new_test_id = generate_test_id(
                gen_date.isoformat(),
                gen_distance_m,
                gen_calibre,
                gen_rifle,
                gen_case_brand,
                gen_bullet_brand,
                gen_bullet_model,
                gen_bullet_weight,
                gen_powder_brand,
                gen_powder_model,
                gen_powder_charge,
                gen_coal,
                gen_primer_brand,
                gen_primer_model
            )
            
            st.session_state.generated_test_id = new_test_id
            st.success(f"Generated Test ID: {new_test_id}")
            st.info("Click 'Save Test Data' to create the test folder and save the data.")
            
            # Update test_id in test_data
            test_data["test_id"] = new_test_id
            
            # Update the form fields with the generated values
            test_data["date"] = gen_date.isoformat()
            test_data["distance_m"] = gen_distance_m
            test_data["platform"]["calibre"] = gen_calibre
            test_data["platform"]["rifle"] = gen_rifle
            test_data["ammo"]["case"]["brand"] = gen_case_brand
            test_data["ammo"]["bullet"]["brand"] = gen_bullet_brand
            test_data["ammo"]["bullet"]["model"] = gen_bullet_model
            test_data["ammo"]["bullet"]["weight_gr"] = gen_bullet_weight
            test_data["ammo"]["powder"]["brand"] = gen_powder_brand
            test_data["ammo"]["powder"]["model"] = gen_powder_model
            test_data["ammo"]["powder"]["charge_gr"] = gen_powder_charge
            test_data["ammo"]["coal_in"] = gen_coal
            test_data["ammo"]["primer"]["brand"] = gen_primer_brand
            test_data["ammo"]["primer"]["model"] = gen_primer_model
    
    # Display current test ID
    if test_id:
        st.subheader("Current Test ID")
        st.code(test_id)
        test_data["test_id"] = test_id
    elif hasattr(st.session_state, 'generated_test_id'):
        st.subheader("Generated Test ID")
        st.code(st.session_state.generated_test_id)
        test_data["test_id"] = st.session_state.generated_test_id
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📋 Test Info", 
        "🔫 Platform", 
        "🧪 Ammunition", 
        "🌡️ Environment", 
        "🎯 Results", 
        "📝 Notes"
    ])
    
    # Main form - moved outside of tabs
    with st.form("test_data_form"):
        
        # Tab 1: Test Information
        with tab1:
            st.header("Test Information")
            
            col1, col2 = st.columns(2)
            with col1:
                date = st.date_input(
                    "Date", 
                    value=datetime.date.fromisoformat(test_data["date"]) if test_data["date"] else datetime.date.today()
                )
            with col2:
                distance_m = st.number_input(
                    "Distance (m)", 
                    min_value=0, 
                    value=int(test_data["distance_m"]),
                    step=25
                )
        
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
            
            # COAL
            st.subheader("Cartridge Measurements")
            test_data["ammo"]["coal_in"] = st.number_input(
                "Cartridge Overall Length (inches)", 
                min_value=0.0, 
                value=float(test_data["ammo"]["coal_in"]),
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
                test_data["group"]["group_es_mm"] = st.number_input(
                    "Group Extreme Spread (mm)", 
                    min_value=0.0, 
                    value=float(test_data["group"]["group_es_mm"]),
                    step=0.1
                )
                test_data["group"]["group_es_moa"] = st.number_input(
                    "Group Extreme Spread (MOA)", 
                    min_value=0.0, 
                    value=float(test_data["group"]["group_es_moa"]),
                    step=0.01
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
        
        # Submit button - make it more prominent
        st.markdown("---")  # Add a separator
        st.markdown("### Save your changes")
        st.markdown("") # Add extra space
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submitted = st.form_submit_button("Save Test Data", use_container_width=True)
        st.markdown("") # Add extra space
        
        if submitted:
            if not test_data["test_id"]:
                st.error("Test ID is required. Please select an existing test or generate a new test ID.")
            else:
                # Save the data
                utils.save_test_data(test_data["test_id"], test_data)
                st.success(f"Test data for '{test_data['test_id']}' saved successfully!")
                
                # If files were specified, check if they exist in the test folder
                test_folder = os.path.join("tests", test_data["test_id"])
                if test_data["files"]["chrono_csv"] and not os.path.exists(os.path.join(test_folder, test_data["files"]["chrono_csv"])):
                    st.warning(f"Note: Chronograph CSV file '{test_data['files']['chrono_csv']}' not found in test folder.")
                if test_data["files"]["target_photo"] and not os.path.exists(os.path.join(test_folder, test_data["files"]["target_photo"])):
                    st.warning(f"Note: Target photo '{test_data['files']['target_photo']}' not found in test folder.")


if __name__ == "__main__":
    main()
