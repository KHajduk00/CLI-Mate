import os
import json
import time
from pathlib import Path

def get_package_root():
    """Get the absolute path to the package root directory."""
    return str(Path(__file__).parent.absolute())

def load_config(config_name='config.json'):
    """Load configuration from JSON file."""
    config_path = os.path.join(get_package_root(), config_name)
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Configuration file '{config_name}' not found at {config_path}. "
            "Please ensure it exists and contains valid API_KEY and CITY values."
        )

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_current_time():
    """Get current time in HH:MM format."""
    return time.strftime("%H:%M")
    