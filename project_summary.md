# Precision Rifle Load Development App

## Project Overview
This Streamlit application manages precision rifle load development test data. It allows users to browse test folders, load and edit YAML files, display them in a structured form, and save changes back. The application includes dropdown lists for common components and an admin interface for managing these lists.

## Project Structure
```
Reloading/
├── app.py              ← main Streamlit app
├── admin.py            ← component list admin interface
├── editor.py           ← form components
├── utils.py            ← YAML load/save functions
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

4. **Admin Interface**
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
- Fixed powder charge precision in folder names to maintain 2 decimal places
- Added Gordon GRT analysis image display in the Results tab
- Improved UI readability with clearer section separation between ammunition components
- Fixed slider errors in analysis.py to ensure min and max values are always different
- Added horizontal separator lines between sections in the Ammunition tab
- Enhanced data analysis charts with detailed x-axis labels:
  - Added numbered extensions for tests on the same date (e.g., "09/04/2025 - 01", "09/04/2025 - 02")
  - Included test index, powder charge, and COAL in labels for easy identification
  - Split labels into two lines for better readability
  - Applied consistent formatting across all charts
