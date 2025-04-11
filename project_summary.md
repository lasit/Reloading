# Precision Rifle Load Development App

## Project Overview
This Streamlit application manages precision rifle load development test data. It allows users to browse test folders, load and edit YAML files, display them in a structured form, and save changes back. The application includes dropdown lists for common components and an admin interface for managing these lists.

## Application Pages
The application is split into three Streamlit pages, each serving a specific purpose:

1. **Main App** (http://localhost:8501)
   - For managing test data and creating new tests
   - Primary interface for data entry and test management

2. **Data Analysis** (http://localhost:8502)
   - For analyzing and visualizing test data
   - Interactive charts and filtering capabilities

3. **Admin Interface** (http://localhost:8503)
   - For managing component lists and options
   - Add, edit, and delete component options

Each page can be accessed through its respective URL or through the navigation buttons in the sidebar of any page.

## Project Structure
```
Reloading/
├── app.py              ← main Streamlit app
├── admin.py            ← component list admin interface
├── analysis.py         ← data analysis and visualization
├── editor.py           ← form components
├── utils.py            ← YAML load/save functions
├── start_apps.py       ← Python script to start all apps
├── start_apps.sh       ← Shell script to start all apps
├── Component_List.yaml ← dropdown list data
├── requirements.txt    ← dependencies
├── README.md           ← project documentation
└── tests/              ← test data folders
    └── [test-folders]/ ← individual test folders
        ├── group.yaml  ← test data in YAML format
        ├── chrono.csv  ← chronograph data
        ├── target.jpg  ← target image
        └── notes.md    ← additional notes
```

## Features Implemented
1. **Test Data Management**
   - Browse existing tests via sidebar
   - Search and filter tests by test ID
   - Create new tests with auto-generated IDs
   - Load and save YAML data with correct structure
   - Parse test ID components automatically
   - Form validation with required fields
   - Immediate data saving after test ID generation

2. **User Interface**
   - Tabbed interface with intuitive icons
   - Sidebar for test selection with search functionality
   - Form validation and error handling
   - Responsive layout with columns
   - Dropdown lists for common components
   - Custom value option for all dropdown lists

3. **Data Processing**
   - Automatic MOA calculation
   - Test ID generation from components
   - File existence checking
   - Component list management

4. **Data Analysis and Visualization**
   - Comprehensive filtering system for all test parameters
   - Interactive data tables for comparing test results
   - Multiple visualization options:
     - Separate charts for accuracy metrics (Group Size and Mean Radius)
     - Separate charts for velocity metrics (Average Velocity, ES, and SD)
     - Combined multi-axis chart showing all 5 key metrics together
   - Detailed x-axis labels with date, test index, powder charge, and COAL
   - Multi-line labels for improved readability
   - Automatic detection of tests conducted on the same date with sequential numbering

5. **Admin Interface**
   - Dedicated admin page for managing component lists
   - Add, edit, and delete items in component lists
   - Organized by component type in tabs

## Technical Details
- **Data Structure**: The app uses a consistent data structure for all test data, including:
  - Test metadata (date, distance)
  - Platform configuration (rifle, calibre)
  - Ammunition configuration (bullet, powder, primer, case)
  - Environmental conditions
  - Group results
  - Chronograph results
  - File paths
  - Notes

- **Component Lists**: The app maintains lists of common components in Component_List.yaml:
  - Calibre options
  - Rifle options
  - Case brand options
  - Powder brand and model options
  - Bullet brand and model options
  - Primer brand and model options

- **File Naming Convention**: Test folders follow this format:
  `[Date]__[Distance]_[Calibre]_[Rifle]_[CaseBrand]_[BulletBrand]_[BulletModel]_[BulletWeight]_[PowderBrand]_[Powder]_[Charge]_[COAL]_[PrimerBrand]_[Primer]`

- **Dependencies**:
  - streamlit==1.32.0
  - pyyaml==6.0.1
  - matplotlib==3.9.4
  - streamlit-aggrid==0.3.4

- **Application Startup**:
  - The application can be started using either:
    - `python3 start_apps.py`: Python script that starts all three Streamlit applications simultaneously, with proper error handling and logging
    - `bash start_apps.sh`: Shell script alternative for starting all applications
  - Each script starts the three applications on their respective ports:
    - Main App on port 8501
    - Data Analysis on port 8502
    - Admin Interface on port 8503
  - Both scripts provide console output with URLs to access each application


## Development History
- Created basic app structure with app.py editor.py and utils.py
- Implemented YAML loading and saving functionality
- Created form UI with tabs and sections
- Added test ID generation and parsing
- Implemented MOA calculation
- Added file existence checking
- Added form validation for required fields
- Implemented immediate data saving after test ID generation
- Created Component_List.yaml for dropdown options
- Replaced text inputs with dropdown lists for common components
- Added admin.py for managing component lists
- Fixed navigation between main app and admin page
- Added GitHub repository with documentation
- Added Cartridge Base to Ogive (B2O) measurement field
- Renamed "Cartridge Overall Length" to "Cartridge Overall Length - COAL (inches)"
- Reorganized UI in Results tab for better grouping of related fields
- Updated test selection to show full test ID including date
- Added sorting of test list by date and then by distance
- Created script to generate random test data for development and testing
- Added Data Analysis page with filtering capabilities for all test parameters
- Implemented test comparison functionality with tabular data display
- Added data visualization with interactive charts:
  - Group Size and Mean Radius over time chart
  - Velocity metrics (Average, ES, SD) over time chart
  - Tabbed interface for different chart types
- Enhanced data visualization with a combined multi-axis chart showing all 5 metrics:
  - Group Size (MOA)
  - Mean Radius (mm)
  - Average Velocity (fps)
  - Extreme Spread (ES)
  - Standard Deviation (SD)
- Reorganized visualization interface with separate and combined chart views
- Updated COAL and B2O measurements to display with 3 decimal places in test IDs for greater precision
- Added custom YAML representer to preserve 3 decimal places in float values when saving data
- Added format="%.3f" to COAL and B2O number input fields to maintain 3 decimal places in the UI
- Made B2O a required field when creating a new test, similar to COAL
- Changed powder charge precision in folder names to use integer values instead of 2 decimal places
- Added code to parse B2O values from test IDs
- Improved UI readability with clearer section separation between ammunition components
- Fixed slider errors in analysis.py to ensure min and max values are always different
- Enhanced data analysis charts with detailed x-axis labels:
  - Added numbered extensions for tests on the same date (e.g., "09/04/2025 - 01", "09/04/2025 - 02")
  - Included test index, powder charge, and COAL in labels for easy identification
  - Split labels into two lines for better readability
  - Applied consistent formatting across all charts
- Created application startup scripts for improved user experience:
  - Added start_apps.py with robust error handling, logging, and graceful shutdown
  - Added start_apps.sh as a shell script alternative
  - Both scripts automatically start all three application components simultaneously
