#!/usr/bin/env python3
"""
Weather Station Application
--------------------------
Main entry point for the weather station application.
Handles initialization and running of the weather monitoring system.
"""

import sys
import logging
from pathlib import Path
from weather import WeatherStation
from utilities import load_config

def setup_logging():
    """Configure logging for the application."""
    # Create logs directory if it doesn't exist
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)

    # Create log file path
    log_file = log_dir / 'weather_station.log'

    try:
        logging.basicConfig(
            level=logging.DEBUG,  # Adjust logging level as needed
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, mode='a', encoding='utf-8')
                # Removed StreamHandler to disable terminal output
            ]
        )
        logger = logging.getLogger('WeatherStation')
        logger.info("Logging system initialized")
        return logger
    except Exception as e:
        print(f"Error setting up logging: {str(e)}")
        sys.exit(1)

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
        # Setup logging first
        logger = setup_logging()
        logger.info("Starting Weather Station application...")

        # Verify configuration
        check_configuration()
        logger.info("Configuration verified successfully")

        # Initialize and run weather station
        weather_station = WeatherStation()
        logger.info("Weather Station initialized successfully")

        # Start the weather dashboard
        weather_station.display_weather_dashboard()

    except KeyboardInterrupt:
        if 'logger' in locals():
            logger.info("Application terminated by user")
        print("\nApplication terminated by user")
        sys.exit(0)
    except Exception as e:
        if 'logger' in locals():
            logger.error(f"An error occurred: {str(e)}")
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()

