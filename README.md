# Precision Rifle Load Development

A Streamlit application for tracking and analyzing precision rifle load development data.

## Features

- Create and manage test data for different rifle loads
- Track important parameters like:
  - Platform details (caliber, rifle, barrel length, twist rate)
  - Ammunition components (case, bullet, powder, primer)
  - Environmental conditions
  - Group measurements and chronograph data
- Generate unique test IDs based on load components
- Form validation to ensure complete data entry
- Search and filter existing tests

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/lasit/Reloading.git
   cd Reloading
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   streamlit run app.py
   ```

## Usage

1. Create a new test by checking the "Create new test" checkbox in the sidebar
2. Fill in all required fields marked with an asterisk (*)
3. Click "Generate Test ID" to create a unique identifier for your test
4. Fill in additional details in the tabs (Test Info, Platform, Ammunition, Environment, Results, Notes)
5. Click "Save Test Data" to save your test data

## Project Structure

- `app.py`: Main Streamlit application
- `utils.py`: Utility functions for data handling
- `editor.py`: Editor functionality
- `tests/`: Directory containing test data folders

## License

[MIT License](LICENSE)
