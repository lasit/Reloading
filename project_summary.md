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

## Future Enhancements
- Add image preview for target photos
- Implement CSV parsing for chronograph data
- Add validation for input fields
- Implement auto-calculation of more fields
- Add more graph types to the Data Analysis page:
  - Scatter plots comparing powder charge vs. velocity
  - Scatter plots comparing powder charge vs. group size
  - Bar charts for comparing different loads
  - Heat maps for environmental factors vs. accuracy

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
