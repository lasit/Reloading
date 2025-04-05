import os
import yaml
from typing import Dict, List, Any, Optional


def load_yaml(file_path: str) -> Dict[str, Any]:
    """
    Load a YAML file and return its contents as a dictionary.
    
    Args:
        file_path: Path to the YAML file
        
    Returns:
        Dictionary containing the YAML file contents
    """
    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
            return data if data else {}
    except FileNotFoundError:
        return {}


def save_yaml(file_path: str, data: Dict[str, Any]) -> None:
    """
    Save a dictionary to a YAML file.
    
    Args:
        file_path: Path where the YAML file will be saved
        data: Dictionary to save as YAML
    """
    # Ensure the directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    with open(file_path, 'w') as file:
        yaml.dump(data, file, default_flow_style=False, sort_keys=False)


def get_test_folders() -> List[str]:
    """
    Get a list of all test folders in the tests directory.
    
    Returns:
        List of test folder names
    """
    tests_dir = "tests"
    if not os.path.exists(tests_dir):
        os.makedirs(tests_dir, exist_ok=True)
        return []
    
    return [folder for folder in os.listdir(tests_dir) 
            if os.path.isdir(os.path.join(tests_dir, folder))]


def get_test_file_path(test_name: str) -> str:
    """
    Get the path to a test's YAML file.
    
    Args:
        test_name: Name of the test
        
    Returns:
        Path to the test's YAML file
    """
    return os.path.join("tests", test_name, "group.yaml")


def create_test_folder(test_name: str) -> str:
    """
    Create a new test folder.
    
    Args:
        test_name: Name of the test folder to create
        
    Returns:
        Path to the created test folder
    """
    folder_path = os.path.join("tests", test_name)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path


def get_test_data(test_name: str) -> Dict[str, Any]:
    """
    Get the data for a specific test.
    
    Args:
        test_name: Name of the test
        
    Returns:
        Dictionary containing the test data
    """
    file_path = get_test_file_path(test_name)
    return load_yaml(file_path)


def save_test_data(test_name: str, data: Dict[str, Any]) -> None:
    """
    Save data for a specific test.
    
    Args:
        test_name: Name of the test
        data: Dictionary containing the test data
    """
    create_test_folder(test_name)
    file_path = get_test_file_path(test_name)
    save_yaml(file_path, data)
