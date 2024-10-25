import time
import requests
import csv
from datetime import datetime, timedelta
from pathlib import Path
from ascii_art import Colors, get_ascii_weather_icon, generate_time_display
from data_logger import format_weather_data, format_air_quality_data
from utilities import load_config, clear_screen, get_current_time

class WeatherStation:
    def __init__(self):
        config = load_config()
        self.api_key = config['API_KEY']
        self.city = config['CITY']
        self.weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={self.api_key}&units=metric'
        self.geo_url = f'http://api.openweathermap.org/geo/1.0/direct?q={self.city}&limit=1&appid={self.api_key}'
        
        # Initialize CSV for data persistence
        self.city_name = self.get_city_name()
        self.csv_file = self.initialize_csv(self.city_name)  # Ensure data directory and CSV file are created
        
        # Initialize last save time
        self.last_save_time = datetime.now()

    def get_city_name(self):
        """Get the city name from the config file."""
        return self.city.replace(' ', '_').lower()

    def initialize_csv(self, city):
        """Create data directory and city-specific CSV file with headers if they don't exist."""
        data_dir = Path('data')
        data_dir.mkdir(exist_ok=True)

        csv_file = data_dir / f'{city}_weather_data.csv'

        if not csv_file.exists():
            headers = [
                'Time', 'Temperature', 'Feels Like', 'Humidity', 'Pressure',
                'Visibility', 'Wind Speed', 'Clouds', 'Rain', 'AQI',
                'CO', 'NO', 'NO2', 'O3', 'SO2', 'PM2.5', 'PM10', 'NH3'
            ]

            with open(csv_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(headers)

        return csv_file

    def save_data(self, weather_data, aqi_index, components):
        """Save weather and air quality data to city-specific CSV file."""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            row = [
                timestamp,
                weather_data['temperature'],
                weather_data['feels_like'],
                weather_data['humidity'],
                weather_data['pressure'],
                weather_data['visibility'],
                weather_data['wind_speed'],
                weather_data['clouds'],
                weather_data['rain'],
                aqi_index,
                components['co'],
                components['no'],
                components['no2'],
                components['o3'],
                components['so2'],
                components['pm2_5'],
                components['pm10'],
                components['nh3']
            ]

            with open(self.csv_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(row)

            print(f"Data saved successfully for {self.city} at {timestamp}")

        except Exception as e:
            print(f"Error saving data: {str(e)}")

    def get_weather_data(self):
        """Fetch weather data from OpenWeatherMap API."""
        try:
            response = requests.get(self.weather_url)
            response.raise_for_status()
            data = response.json()

            return {
                'weather_icon': data['weather'][0]['icon'],
                'temperature': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'visibility': data['visibility'],
                'wind_speed': data['wind']['speed'],
                'clouds': data['clouds']['all'],
                'rain': data['rain']['1h'] if 'rain' in data else "No Data",
                'lat': data['coord']['lat'],
                'lon': data['coord']['lon']
            }
        except requests.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None

    def get_air_quality(self, lat, lon):
        """Fetch air quality data from OpenWeatherMap API."""
        air_quality_url = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={self.api_key}'
        try:
            response = requests.get(air_quality_url)
            response.raise_for_status()
            data = response.json()
            return data['list'][0]['main']['aqi'], data['list'][0]['components']
        except requests.RequestException as e:
            print(f"Error fetching air quality data: {e}")
            return None, None

    def display_weather_dashboard(self):
        """Display weather dashboard with continuous updates."""
        while True:
            clear_screen()
            current_time = get_current_time()

            # Display time
            time_display = generate_time_display(current_time)
            for row in time_display:
                print(Colors.BOLD + Colors.GREEN + row + Colors.RESET)

            # Get and display weather data
            weather_data = self.get_weather_data()
            if weather_data:
                weather_icon = get_ascii_weather_icon(weather_data['weather_icon'])
                print(f"\nWeather: {weather_icon}")

                # Display weather information
                for line in format_weather_data(weather_data, self.city):
                    print(line)

                # Get and display air quality
                aqi_index, components = self.get_air_quality(weather_data['lat'], weather_data['lon'])
                for line in format_air_quality_data(aqi_index, components):
                    print(line)

                # Save data to CSV if an hour has passed since the last save
                if datetime.now() - self.last_save_time >= timedelta(hours=1):
                    self.save_data(weather_data, aqi_index, components)
                    self.last_save_time = datetime.now()  # Update last save time

            time.sleep(60)  # Update every minute

def main():
    weather_station = WeatherStation()
    weather_station.display_weather_dashboard()

if __name__ == "__main__":
    main()

