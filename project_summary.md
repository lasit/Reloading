# Precision Rifle Load Development App

## Project Overview
This Streamlit application manages precision rifle load development test data. It allows users to browse test folders, load and edit YAML files, display them in a structured form, and save changes back.

## Project Structure
```
Reloading/
├── app.py              ← main Streamlit app
├── editor.py           ← form components
├── utils.py            ← YAML load/save functions
├── requirements.txt    ← dependencies
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

2. **User Interface**
   - Tabbed interface with intuitive icons
   - Sidebar for test selection with search functionality
   - Form validation and error handling
   - Responsive layout with columns

3. **Data Processing**
   - Automatic MOA calculation
   - Test ID generation from components
   - File existence checking

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

- **File Naming Convention**: Test folders follow this format:
  `[Date]__[Distance]_[Calibre]_[Rifle]_[BulletModel]_[BulletWeight]_[Powder]_[Charge]_[COAL]_[Primer]`

- **Dependencies**:
  - streamlit==1.32.0
  - pyyaml==6.0.1

## Future Enhancements
- Add image preview for target photos
- Implement CSV parsing for chronograph data
- Add data visualization for group measurements
- Create a comparison view for multiple tests
- Add validation for input fields
- Implement auto-calculation of more fields

## Development History
- Created basic app structure with app.py, editor.py, and utils.py
- Implemented YAML loading and saving functionality
- Created form UI with tabs and sections
- Added test ID generation and parsing
- Implemented MOA calculation
- Added file existence checking
- Refactored code for better organization
