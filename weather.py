import time
import requests
from ascii_art import Colors, get_ascii_weather_icon, generate_time_display
from utilities import load_config, clear_screen, get_current_time

class WeatherStation:
    def __init__(self):
        config = load_config()
        self.api_key = config['API_KEY']
        self.city = config['CITY']
        self.weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={self.api_key}&units=metric'

    def format_weather_data(self, weather_data):
        """Format weather data for display."""
        if weather_data is None:
            return ["Could not retrieve weather data."]

        temp_color = self.get_temp_color(weather_data['temperature'])
        feels_like_color = self.get_temp_color(weather_data['feels_like'])

        lines = [
            f"\nCurrent temperature in {self.city}: " + temp_color + f"{weather_data['temperature']}°C " + Colors.RESET + f"(Feels like: " + feels_like_color + f"{weather_data['feels_like']}°C" + Colors.RESET + ")",
            f"Humidity: {weather_data['humidity']}%",
            f"Pressure: {weather_data['pressure']} hPa",
            f"Visibility: {weather_data['visibility']} meters",
            f"Wind speed: {weather_data['wind_speed']} m/s",
            f"Clouds: {weather_data['clouds']}%",
            f"Rain (last 1 hour): {weather_data['rain']} mm"
        ]
        return lines

    def get_temp_color(self, temp):
        if int(temp) >= 25:
            return Colors.RED
        elif int(temp) in range(15, 25):
            return Colors.YELLOW
        else:
            return Colors.BLUE

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

    def format_air_quality_data(self, aqi_index, components):
        """Format air quality data for display."""
        if aqi_index is None or components is None:
            return ["Could not retrieve air quality data."]

        aqi_map = {
            '1': "(Good)",
            '2': "(Fair)",
            '3': "(Moderate)",
            '4': "(Poor)",
            '5': "(Very Poor)"
        }
        
        aqi_description = aqi_map.get(str(aqi_index), "(Unknown)")
        lines = [
            f"\nAir Quality Index (AQI): {aqi_index} {aqi_description}",
            f"CO: {components['co']} μg/m³",
            f"NO: {components['no']} μg/m³",
            f"NO2: {components['no2']} μg/m³",
            f"O3: {components['o3']} μg/m³",
            f"SO2: {components['so2']} μg/m³",
            f"PM2.5: {components['pm2_5']} μg/m³",
            f"PM10: {components['pm10']} μg/m³",
            f"NH3: {components['nh3']} μg/m³"
        ]
        return lines

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
                for line in self.format_weather_data(weather_data):
                    print(line)

                # Get and display air quality
                aqi_index, components = self.get_air_quality(weather_data['lat'], weather_data['lon'])
                for line in self.format_air_quality_data(aqi_index, components):
                    print(line)

            time.sleep(60)  # Update every minute

def main():
    weather_station = WeatherStation()
    weather_station.display_weather_dashboard()

if __name__ == "__main__":
    main()
