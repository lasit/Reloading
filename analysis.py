import streamlit as st
import os
import yaml
import datetime
import pandas as pd
import utils
from utils import load_component_lists

def load_all_test_data():
    """
    Load all test data from the tests directory into a pandas DataFrame.
    
    Returns:
        DataFrame containing all test data
    """
    test_folders = utils.get_test_folders()
    all_data = []
    
    for test_id in test_folders:
        try:
            data = utils.get_test_data(test_id)
            if data:
                # Flatten the nested structure for easier filtering
                flat_data = {
                    "test_id": test_id,
                    "date": data.get("date", ""),
                    "distance_m": data.get("distance_m", 0),
                    
                    # Platform
                    "calibre": data.get("platform", {}).get("calibre", ""),
                    "rifle": data.get("platform", {}).get("rifle", ""),
                    "barrel_length_in": data.get("platform", {}).get("barrel_length_in", 0.0),
                    "twist_rate": data.get("platform", {}).get("twist_rate", ""),
                    
                    # Ammo - Case
                    "case_brand": data.get("ammo", {}).get("case", {}).get("brand", ""),
                    "case_lot": data.get("ammo", {}).get("case", {}).get("lot", ""),
                    "neck_turned": data.get("ammo", {}).get("case", {}).get("neck_turned", ""),
                    "brass_sizing": data.get("ammo", {}).get("case", {}).get("brass_sizing", ""),
                    "bushing_size": data.get("ammo", {}).get("case", {}).get("bushing_size", 0.0),
                    "shoulder_bump": data.get("ammo", {}).get("case", {}).get("shoulder_bump", 0.0),
                    
                    # Ammo - Bullet
                    "bullet_brand": data.get("ammo", {}).get("bullet", {}).get("brand", ""),
                    "bullet_model": data.get("ammo", {}).get("bullet", {}).get("model", ""),
                    "bullet_weight_gr": data.get("ammo", {}).get("bullet", {}).get("weight_gr", 0.0),
                    "bullet_lot": data.get("ammo", {}).get("bullet", {}).get("lot", ""),
                    
                    # Ammo - Powder
                    "powder_brand": data.get("ammo", {}).get("powder", {}).get("brand", ""),
                    "powder_model": data.get("ammo", {}).get("powder", {}).get("model", ""),
                    "powder_charge_gr": data.get("ammo", {}).get("powder", {}).get("charge_gr", 0.0),
                    "powder_lot": data.get("ammo", {}).get("powder", {}).get("lot", ""),
                    
                    # Ammo - Primer
                    "primer_brand": data.get("ammo", {}).get("primer", {}).get("brand", ""),
                    "primer_model": data.get("ammo", {}).get("primer", {}).get("model", ""),
                    "primer_lot": data.get("ammo", {}).get("primer", {}).get("lot", ""),
                    
                    # Ammo - Cartridge Measurements
                    "coal_in": data.get("ammo", {}).get("coal_in", 0.0),
                    "b2o_in": data.get("ammo", {}).get("b2o_in", 0.0),
                    
                    # Environment
                    "temperature_c": data.get("environment", {}).get("temperature_c", 0.0),
                    "humidity_percent": data.get("environment", {}).get("humidity_percent", 0),
                    "pressure_hpa": data.get("environment", {}).get("pressure_hpa", 0),
                    "wind_speed_mps": data.get("environment", {}).get("wind_speed_mps", 0.0),
                    "wind_dir_deg": data.get("environment", {}).get("wind_dir_deg", 0),
                    "weather": data.get("environment", {}).get("weather", ""),
                    
                    # Group
                    "shots": data.get("group", {}).get("shots", 0),
                    "group_es_mm": data.get("group", {}).get("group_es_mm", 0.0),
                    "group_es_moa": data.get("group", {}).get("group_es_moa", 0.0),
                    "group_es_x_mm": data.get("group", {}).get("group_es_x_mm", 0.0),
                    "group_es_y_mm": data.get("group", {}).get("group_es_y_mm", 0.0),
                    "mean_radius_mm": data.get("group", {}).get("mean_radius_mm", 0.0),
                    "poi_x_mm": data.get("group", {}).get("poi_x_mm", 0.0),
                    "poi_y_mm": data.get("group", {}).get("poi_y_mm", 0.0),
                    
                    # Chrono
                    "avg_velocity_fps": data.get("chrono", {}).get("avg_velocity_fps", 0.0),
                    "sd_fps": data.get("chrono", {}).get("sd_fps", 0.0),
                    "es_fps": data.get("chrono", {}).get("es_fps", 0.0),
                    
                    # Notes
                    "notes": data.get("notes", "")
                }
                all_data.append(flat_data)
        except Exception as e:
            print(f"Error loading test data for {test_id}: {e}")
    
    return pd.DataFrame(all_data)

def main():
    st.set_page_config(
        page_title="Precision Load Development - Data Analysis",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    
    st.title("Precision Rifle Load Development - Data Analysis")
    st.markdown("---")
    
    # Add a link back to the main app
    st.sidebar.markdown("### Navigation")
    if st.sidebar.button("Back to Main App"):
        import webbrowser
        webbrowser.open("http://localhost:8501")
    
    # Load component lists for dropdown menus
    component_lists = load_component_lists()
    
    # Load all test data
    with st.spinner("Loading test data..."):
        df = load_all_test_data()
    
    # Display the number of tests loaded
    st.sidebar.markdown(f"### {len(df)} Tests Loaded")
    
    # Create filter section
    st.header("Filter Tests")
    st.markdown("Select filter criteria to narrow down the tests. Leave a filter empty to include all values.")
    
    # Create filter UI with multiple columns for better space usage
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Test Info")
        
        # Date range filter
        min_date = df["date"].min() if not df.empty else datetime.date.today().isoformat()
        max_date = df["date"].max() if not df.empty else datetime.date.today().isoformat()
        
        date_range = st.date_input(
            "Date Range",
            value=(
                datetime.date.fromisoformat(min_date) if isinstance(min_date, str) else datetime.date.today(),
                datetime.date.fromisoformat(max_date) if isinstance(max_date, str) else datetime.date.today()
            ),
            key="date_range"
        )
        
        # Distance range filter
        distance_range = st.slider(
            "Distance Range (m)",
            min_value=int(df["distance_m"].min()) if not df.empty else 0,
            max_value=int(df["distance_m"].max()) if not df.empty else 1000,
            value=(int(df["distance_m"].min()) if not df.empty else 0, 
                   int(df["distance_m"].max()) if not df.empty else 1000),
            step=100
        )
        
        st.subheader("Platform")
        
        # Calibre filter
        calibre_options = ["All"] + sorted(df["calibre"].unique().tolist())
        selected_calibre = st.selectbox("Calibre", options=calibre_options)
        
        # Rifle filter
        rifle_options = ["All"] + sorted(df["rifle"].unique().tolist())
        selected_rifle = st.selectbox("Rifle", options=rifle_options)
        
        # Twist rate filter
        twist_rate_options = ["All"] + sorted(df["twist_rate"].unique().tolist())
        selected_twist_rate = st.selectbox("Twist Rate", options=twist_rate_options)
    
    with col2:
        st.subheader("Ammunition")
        
        # Case brand filter
        case_brand_options = ["All"] + sorted(df["case_brand"].unique().tolist())
        selected_case_brand = st.selectbox("Case Brand", options=case_brand_options)
        
        # Bullet brand filter
        bullet_brand_options = ["All"] + sorted(df["bullet_brand"].unique().tolist())
        selected_bullet_brand = st.selectbox("Bullet Brand", options=bullet_brand_options)
        
        # Bullet model filter
        bullet_model_options = ["All"] + sorted(df["bullet_model"].unique().tolist())
        selected_bullet_model = st.selectbox("Bullet Model", options=bullet_model_options)
        
        # Bullet weight filter
        bullet_weight_options = ["All"] + sorted(df["bullet_weight_gr"].unique().tolist())
        selected_bullet_weight = st.selectbox("Bullet Weight (gr)", options=bullet_weight_options)
        
        # Powder brand filter
        powder_brand_options = ["All"] + sorted(df["powder_brand"].unique().tolist())
        selected_powder_brand = st.selectbox("Powder Brand", options=powder_brand_options)
        
        # Powder model filter
        powder_model_options = ["All"] + sorted(df["powder_model"].unique().tolist())
        selected_powder_model = st.selectbox("Powder Model", options=powder_model_options)
        
        # Primer brand filter
        primer_brand_options = ["All"] + sorted(df["primer_brand"].unique().tolist())
        selected_primer_brand = st.selectbox("Primer Brand", options=primer_brand_options)
        
        # Primer model filter
        primer_model_options = ["All"] + sorted(df["primer_model"].unique().tolist())
        selected_primer_model = st.selectbox("Primer Model", options=primer_model_options)
    
    with col3:
        st.subheader("Environment")
        
        # Temperature range filter
        temp_range = st.slider(
            "Temperature Range (°C)",
            min_value=float(df["temperature_c"].min()) if not df.empty else 0.0,
            max_value=float(df["temperature_c"].max()) if not df.empty else 40.0,
            value=(float(df["temperature_c"].min()) if not df.empty else 0.0, 
                   float(df["temperature_c"].max()) if not df.empty else 40.0),
            step=1.0
        )
        
        # Wind speed range filter
        wind_range = st.slider(
            "Wind Speed Range (m/s)",
            min_value=float(df["wind_speed_mps"].min()) if not df.empty else 0.0,
            max_value=float(df["wind_speed_mps"].max()) if not df.empty else 10.0,
            value=(float(df["wind_speed_mps"].min()) if not df.empty else 0.0, 
                   float(df["wind_speed_mps"].max()) if not df.empty else 10.0),
            step=1.0
        )
        
        # Weather filter
        weather_options = ["All"] + sorted(df["weather"].unique().tolist())
        selected_weather = st.selectbox("Weather", options=weather_options)
        
        st.subheader("Results")
        
        # Group size range filter
        group_es_range = st.slider(
            "Group Size Range (mm)",
            min_value=float(df["group_es_mm"].min()) if not df.empty else 0.0,
            max_value=float(df["group_es_mm"].max()) if not df.empty else 200.0,
            value=(float(df["group_es_mm"].min()) if not df.empty else 0.0, 
                   float(df["group_es_mm"].max()) if not df.empty else 200.0),
            step=10.0
        )
        
        # Velocity range filter
        velocity_range = st.slider(
            "Velocity Range (fps)",
            min_value=float(df["avg_velocity_fps"].min()) if not df.empty else 0.0,
            max_value=float(df["avg_velocity_fps"].max()) if not df.empty else 3000.0,
            value=(float(df["avg_velocity_fps"].min()) if not df.empty else 0.0, 
                   float(df["avg_velocity_fps"].max()) if not df.empty else 3000.0),
            step=100.0
        )
    
    # Apply filters
    filtered_df = df.copy()
    
    # Date filter
    if len(date_range) == 2:
        start_date, end_date = date_range
        filtered_df = filtered_df[
            (filtered_df["date"] >= start_date.isoformat()) & 
            (filtered_df["date"] <= end_date.isoformat())
        ]
    
    # Distance filter
    filtered_df = filtered_df[
        (filtered_df["distance_m"] >= distance_range[0]) & 
        (filtered_df["distance_m"] <= distance_range[1])
    ]
    
    # Calibre filter
    if selected_calibre != "All":
        filtered_df = filtered_df[filtered_df["calibre"] == selected_calibre]
    
    # Rifle filter
    if selected_rifle != "All":
        filtered_df = filtered_df[filtered_df["rifle"] == selected_rifle]
    
    # Twist rate filter
    if selected_twist_rate != "All":
        filtered_df = filtered_df[filtered_df["twist_rate"] == selected_twist_rate]
    
    # Case brand filter
    if selected_case_brand != "All":
        filtered_df = filtered_df[filtered_df["case_brand"] == selected_case_brand]
    
    # Bullet brand filter
    if selected_bullet_brand != "All":
        filtered_df = filtered_df[filtered_df["bullet_brand"] == selected_bullet_brand]
    
    # Bullet model filter
    if selected_bullet_model != "All":
        filtered_df = filtered_df[filtered_df["bullet_model"] == selected_bullet_model]
    
    # Bullet weight filter
    if selected_bullet_weight != "All":
        filtered_df = filtered_df[filtered_df["bullet_weight_gr"] == selected_bullet_weight]
    
    # Powder brand filter
    if selected_powder_brand != "All":
        filtered_df = filtered_df[filtered_df["powder_brand"] == selected_powder_brand]
    
    # Powder model filter
    if selected_powder_model != "All":
        filtered_df = filtered_df[filtered_df["powder_model"] == selected_powder_model]
    
    # Primer brand filter
    if selected_primer_brand != "All":
        filtered_df = filtered_df[filtered_df["primer_brand"] == selected_primer_brand]
    
    # Primer model filter
    if selected_primer_model != "All":
        filtered_df = filtered_df[filtered_df["primer_model"] == selected_primer_model]
    
    # Temperature filter
    filtered_df = filtered_df[
        (filtered_df["temperature_c"] >= temp_range[0]) & 
        (filtered_df["temperature_c"] <= temp_range[1])
    ]
    
    # Wind speed filter
    filtered_df = filtered_df[
        (filtered_df["wind_speed_mps"] >= wind_range[0]) & 
        (filtered_df["wind_speed_mps"] <= wind_range[1])
    ]
    
    # Weather filter
    if selected_weather != "All":
        filtered_df = filtered_df[filtered_df["weather"] == selected_weather]
    
    # Group size filter
    filtered_df = filtered_df[
        (filtered_df["group_es_mm"] >= group_es_range[0]) & 
        (filtered_df["group_es_mm"] <= group_es_range[1])
    ]
    
    # Velocity filter
    filtered_df = filtered_df[
        (filtered_df["avg_velocity_fps"] >= velocity_range[0]) & 
        (filtered_df["avg_velocity_fps"] <= velocity_range[1])
    ]
    
    # Display filtered results
    st.header("Filtered Tests")
    st.markdown(f"Found **{len(filtered_df)}** tests matching your criteria.")
    
    if not filtered_df.empty:
        # Select columns to display
        display_columns = [
            "test_id", "date", "distance_m", "calibre", "rifle", 
            "bullet_brand", "bullet_model", "bullet_weight_gr", 
            "powder_brand", "powder_model", "powder_charge_gr",
            "group_es_mm", "group_es_moa", "avg_velocity_fps"
        ]
        
        # Display the filtered tests
        st.dataframe(filtered_df[display_columns], use_container_width=True)
        
        # Placeholder for future graphs
        st.header("Data Visualization")
        st.info("Graphs will be added in future updates.")
    else:
        st.warning("No tests match the selected filters. Try adjusting your criteria.")

if __name__ == "__main__":
    main()
