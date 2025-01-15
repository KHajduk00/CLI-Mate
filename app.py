#!/usr/bin/env python3
"""
Weather Station Application
--------------------------
Main entry point for the weather station application.
Handles initialization and running of the weather monitoring system.
"""

import sys
import argparse
from pathlib import Path
from weather import WeatherStation
from utilities import load_config

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='CLI-mate: A terminal weather dashboard',
        prog='cli-mate'
    )
    
    parser.add_argument('-c', '--city', 
                       help='Override the city in config.json')
    parser.add_argument('-l', '--live', 
                       action='store_false',
                       help='Enable live updates (default: single update)')
    parser.add_argument('-i', '--interval', 
                       type=int,
                       default=3600,
                       help='Weather data update interval in seconds (default: 3600 - 1 hour). Clock display updates every minute regardless of this setting.')
    parser.add_argument('-v', '--version', 
                       action='version',
                       version='%(prog)s 0.1.0')
    
    return parser.parse_args()

def check_configuration():
    """Verify that all necessary configuration files and dependencies exist."""
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
        # Parse command line arguments
        args = parse_arguments()
        
        # Verify configuration
        check_configuration()

        # Initialize weather station with city from command line if provided
        weather_station = WeatherStation(city=args.city)
        
        # Start the weather dashboard
        weather_station.display_weather_dashboard(
            live_updates=args.live,
            update_interval=args.interval
        )

    except KeyboardInterrupt:
        print("\nApplication terminated by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()