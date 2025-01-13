#!/usr/bin/env python3
"""
Weather Station Application
--------------------------
Main entry point for the weather station application.
Handles initialization and running of the weather monitoring system.
"""

import sys
from pathlib import Path
from weather import WeatherStation
from utilities import load_config

def check_configuration():
    """Verify that all necessary configuration files and dependencies exist."""
    config_path = Path('config.json')
    if not config_path.exists():
        raise FileNotFoundError(
            "Configuration file 'config.json' not found. "
            "Please ensure it exists and contains valid API_KEY and CITY values."
        )

    try:
        config = load_config()
        required_keys = ['API_KEY', 'CITY']
        for key in required_keys:
            if key not in config:
                raise KeyError(f"Missing required configuration key: {key}")
    except Exception as e:
        raise Exception(f"Error loading configuration: {str(e)}")

def main():
    """Main entry point of the application."""
    try:
        # Verify configuration
        check_configuration()

        # Initialize and run weather station
        weather_station = WeatherStation()

        # Start the weather dashboard
        weather_station.display_weather_dashboard()

    except KeyboardInterrupt:
        print("\nApplication terminated by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
