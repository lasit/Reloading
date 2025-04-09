import streamlit as st
import os
import yaml
import datetime
import pandas as pd
import matplotlib.pyplot as plt
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
        min_distance = int(df["distance_m"].min()) if not df.empty else 0
        max_distance = int(df["distance_m"].max()) if not df.empty else 1000
        
        # Ensure max_distance is greater than min_distance to avoid slider error
        if max_distance <= min_distance:
            max_distance = min_distance + 100
            
        distance_range = st.slider(
            "Distance Range (m)",
            min_value=min_distance,
            max_value=max_distance,
            value=(min_distance, max_distance),
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
        min_temp = float(df["temperature_c"].min()) if not df.empty else 0.0
        max_temp = float(df["temperature_c"].max()) if not df.empty else 40.0
        
        # Ensure max_temp is greater than min_temp to avoid slider error
        if max_temp <= min_temp:
            max_temp = min_temp + 10.0
            
        temp_range = st.slider(
            "Temperature Range (°C)",
            min_value=min_temp,
            max_value=max_temp,
            value=(min_temp, max_temp),
            step=1.0
        )
        
        # Wind speed range filter
        min_wind = float(df["wind_speed_mps"].min()) if not df.empty else 0.0
        max_wind = float(df["wind_speed_mps"].max()) if not df.empty else 10.0
        
        # Ensure max_wind is greater than min_wind to avoid slider error
        if max_wind <= min_wind:
            max_wind = min_wind + 5.0
            
        wind_range = st.slider(
            "Wind Speed Range (m/s)",
            min_value=min_wind,
            max_value=max_wind,
            value=(min_wind, max_wind),
            step=1.0
        )
        
        # Weather filter
        weather_options = ["All"] + sorted(df["weather"].unique().tolist())
        selected_weather = st.selectbox("Weather", options=weather_options)
        
        st.subheader("Results")
        
        # Group size range filter
        min_group = float(df["group_es_mm"].min()) if not df.empty else 0.0
        max_group = float(df["group_es_mm"].max()) if not df.empty else 200.0
        
        # Ensure max_group is greater than min_group to avoid slider error
        if max_group <= min_group:
            max_group = min_group + 20.0
            
        group_es_range = st.slider(
            "Group Size Range (mm)",
            min_value=min_group,
            max_value=max_group,
            value=(min_group, max_group),
            step=10.0
        )
        
        # Velocity range filter
        min_velocity = float(df["avg_velocity_fps"].min()) if not df.empty else 0.0
        max_velocity = float(df["avg_velocity_fps"].max()) if not df.empty else 3000.0
        
        # Ensure max_velocity is greater than min_velocity to avoid slider error
        if max_velocity <= min_velocity:
            max_velocity = min_velocity + 500.0
            
        velocity_range = st.slider(
            "Velocity Range (fps)",
            min_value=min_velocity,
            max_value=max_velocity,
            value=(min_velocity, max_velocity),
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
        
        # Data Visualization
        st.header("Data Visualization")
        
        if len(filtered_df) > 1:
            # Convert date strings to datetime objects for proper sorting
            filtered_df['date_obj'] = pd.to_datetime(filtered_df['date'])
            
            # Sort by date
            plot_df = filtered_df.sort_values('date_obj')
            
            # Create tabs for different charts
            chart_tabs = st.tabs(["Separate Charts", "Combined Chart"])
            
            # Tab 1: Separate Charts for Accuracy and Velocity
            with chart_tabs[0]:
                # Accuracy Metrics Chart
                st.subheader("Group Size and Mean Radius Over Time")
                
                # Create the plot
                fig1, ax1 = plt.subplots(figsize=(12, 6))
                
                # Plot group size (MOA) on the left y-axis
                color = 'tab:blue'
                ax1.set_xlabel('Date')
                ax1.set_ylabel('Group Size (MOA)', color=color)
                ax1.plot(plot_df['date_obj'], plot_df['group_es_moa'], 'o-', color=color, label='Group Size (MOA)')
                ax1.tick_params(axis='y', labelcolor=color)
                
                # Create a second y-axis for mean radius
                ax2 = ax1.twinx()
                color = 'tab:red'
                ax2.set_ylabel('Mean Radius (mm)', color=color)
                ax2.plot(plot_df['date_obj'], plot_df['mean_radius_mm'], 'o-', color=color, label='Mean Radius (mm)')
                ax2.tick_params(axis='y', labelcolor=color)
                
                # Rotate x-axis labels for better readability
                plt.xticks(rotation=45)
                
                # Add a title and adjust layout
                plt.title('Group Size and Mean Radius Over Time')
                fig1.tight_layout()
                
                # Add a legend
                lines1, labels1 = ax1.get_legend_handles_labels()
                lines2, labels2 = ax2.get_legend_handles_labels()
                ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
                
                # Display the plot
                st.pyplot(fig1)
                
                # Add explanation
                st.markdown("""
                **Chart Explanation:**
                - **Blue Line (Left Axis)**: Group Size in Minutes of Angle (MOA) - smaller is better
                - **Red Line (Right Axis)**: Mean Radius in millimeters (mm) - smaller is better
                
                This chart shows how your group sizes have changed over time for the filtered test data. 
                Look for downward trends which indicate improving accuracy.
                """)
                
                # Velocity Metrics Chart
                st.subheader("Velocity Metrics Over Time")
                
                # Create the plot
                fig2, ax3 = plt.subplots(figsize=(12, 6))
                
                # Plot average velocity on the left y-axis
                color = 'tab:green'
                ax3.set_xlabel('Date')
                ax3.set_ylabel('Average Velocity (fps)', color=color)
                ax3.plot(plot_df['date_obj'], plot_df['avg_velocity_fps'], 'o-', color=color, label='Avg Velocity (fps)')
                ax3.tick_params(axis='y', labelcolor=color)
                
                # Create a second y-axis for ES and SD
                ax4 = ax3.twinx()
                ax4.set_ylabel('Velocity Variation (fps)')
                
                # Plot ES and SD on the right y-axis with different colors
                ax4.plot(plot_df['date_obj'], plot_df['es_fps'], 'o-', color='tab:orange', label='ES (fps)')
                ax4.plot(plot_df['date_obj'], plot_df['sd_fps'], 'o-', color='tab:purple', label='SD (fps)')
                
                # Rotate x-axis labels for better readability
                plt.xticks(rotation=45)
                
                # Add a title and adjust layout
                plt.title('Velocity Metrics Over Time')
                fig2.tight_layout()
                
                # Add a legend
                lines3, labels3 = ax3.get_legend_handles_labels()
                lines4, labels4 = ax4.get_legend_handles_labels()
                ax3.legend(lines3 + lines4, labels3 + labels4, loc='upper left')
                
                # Display the plot
                st.pyplot(fig2)
                
                # Add explanation
                st.markdown("""
                **Chart Explanation:**
                - **Green Line (Left Axis)**: Average Velocity in feet per second (fps)
                - **Orange Line (Right Axis)**: Extreme Spread (ES) in fps - smaller is better
                - **Purple Line (Right Axis)**: Standard Deviation (SD) in fps - smaller is better
                
                This chart shows how your velocity metrics have changed over time for the filtered test data.
                Look for consistent velocity (flat green line) and low variation (low orange and purple lines).
                """)
            
            # Tab 2: Combined Chart with All Metrics
            with chart_tabs[1]:
                st.subheader("All Metrics Combined")
                
                # Create figure with 5 y-axes
                fig3, ax5 = plt.subplots(figsize=(14, 8))
                
                # Define colors for each metric
                colors = {
                    'group_es_moa': 'tab:blue',
                    'mean_radius_mm': 'tab:red',
                    'avg_velocity_fps': 'tab:green',
                    'es_fps': 'tab:orange',
                    'sd_fps': 'tab:purple'
                }
                
                # First axis - Group Size (MOA)
                ax5.set_xlabel('Date')
                ax5.set_ylabel('Group Size (MOA)', color=colors['group_es_moa'])
                ax5.plot(plot_df['date_obj'], plot_df['group_es_moa'], 'o-', color=colors['group_es_moa'], label='Group Size (MOA)')
                ax5.tick_params(axis='y', labelcolor=colors['group_es_moa'])
                
                # Create additional axes
                ax6 = ax5.twinx()  # Mean Radius
                ax7 = ax5.twinx()  # Average Velocity
                ax8 = ax5.twinx()  # ES
                ax9 = ax5.twinx()  # SD
                
                # Offset the right axes to prevent overlap
                offset = 60
                ax7.spines['right'].set_position(('outward', offset))
                ax8.spines['right'].set_position(('outward', offset * 2))
                ax9.spines['right'].set_position(('outward', offset * 3))
                
                # Mean Radius (mm)
                ax6.set_ylabel('Mean Radius (mm)', color=colors['mean_radius_mm'])
                ax6.plot(plot_df['date_obj'], plot_df['mean_radius_mm'], 'o-', color=colors['mean_radius_mm'], label='Mean Radius (mm)')
                ax6.tick_params(axis='y', labelcolor=colors['mean_radius_mm'])
                
                # Average Velocity (fps)
                ax7.set_ylabel('Avg Velocity (fps)', color=colors['avg_velocity_fps'])
                ax7.plot(plot_df['date_obj'], plot_df['avg_velocity_fps'], 'o-', color=colors['avg_velocity_fps'], label='Avg Velocity (fps)')
                ax7.tick_params(axis='y', labelcolor=colors['avg_velocity_fps'])
                
                # ES (fps)
                ax8.set_ylabel('ES (fps)', color=colors['es_fps'])
                ax8.plot(plot_df['date_obj'], plot_df['es_fps'], 'o-', color=colors['es_fps'], label='ES (fps)')
                ax8.tick_params(axis='y', labelcolor=colors['es_fps'])
                
                # SD (fps)
                ax9.set_ylabel('SD (fps)', color=colors['sd_fps'])
                ax9.plot(plot_df['date_obj'], plot_df['sd_fps'], 'o-', color=colors['sd_fps'], label='SD (fps)')
                ax9.tick_params(axis='y', labelcolor=colors['sd_fps'])
                
                # Rotate x-axis labels for better readability
                plt.xticks(rotation=45)
                
                # Add a title and adjust layout
                plt.title('All Metrics Combined')
                fig3.tight_layout()
                
                # Create a combined legend
                lines = []
                labels = []
                for ax in [ax5, ax6, ax7, ax8, ax9]:
                    lns, lbs = ax.get_legend_handles_labels()
                    lines.extend(lns)
                    labels.extend(lbs)
                
                # Place legend at the top of the chart
                ax5.legend(lines, labels, loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=5)
                
                # Display the plot
                st.pyplot(fig3)
                
                # Add explanation
                st.markdown("""
                **Chart Explanation:**
                - **Blue Line**: Group Size in Minutes of Angle (MOA) - smaller is better
                - **Red Line**: Mean Radius in millimeters (mm) - smaller is better
                - **Green Line**: Average Velocity in feet per second (fps)
                - **Orange Line**: Extreme Spread (ES) in fps - smaller is better
                - **Purple Line**: Standard Deviation (SD) in fps - smaller is better
                
                This combined chart shows all metrics together to help identify correlations between accuracy and velocity.
                For example, you might notice that lower velocity variation (ES and SD) often correlates with better group sizes.
                """)
        else:
            st.info("At least two data points are needed to create meaningful graphs. Adjust your filters to include more tests.")
    else:
        st.warning("No tests match the selected filters. Try adjusting your criteria.")

if __name__ == "__main__":
    main()
