# Weather Station Display

A minimal terminal-based weather station display that shows current time, weather conditions, and air quality data for a specified city. Perfect for Linux rice setups and terminal customization.

## Features

- Real-time display of current time in ASCII art format
- Live weather information including:
  - Temperature (color-coded based on warmth)
  - Weather condition icon
  - Humidity, pressure, and wind data
- Air quality information with AQI and pollutant levels
- Auto-updates every minute
- Clean, terminal-friendly interface

## Requirements

- Python 3.6+
- `requests` library
- OpenWeatherMap API key

## Installation

1. Clone the repository:

  ```bash
  git clone https://github.com/yourusername/CLI-Mate.git
  cd CLI-Mate
  ```

2. Create your config file:

  ```bash
  cp config.json.example config.json
  ```

3. Edit config.json with your OpenWeatherMap API key and preferred city

  ```bash
  nano config.json
  ```

4. Run the installation script:

  ```bash
  ./install.sh
  ```

5. Install the required Python library:

   ```bash
   pip install requests
   ```

## Configuration

Before running the application, you need to create a `config.json` file in the same directory as the script. This file should contain your OpenWeatherMap API key and the city you want to monitor:

```json
{
  "API_KEY": "your_openweathermap_api_key_here",
  "CITY": "Your City Name"
}
```

Replace `"your_openweathermap_api_key_here"` with your actual OpenWeatherMap API key, and `"Your City Name"` with the name of the city you want to monitor.

## Usage

Once installed, you can use CLI-mate from anywhere with these commands:

```
# Show current weather (single update)
cli-mate

# Enable live updates
cli-mate -l

# Change update interval to 30 seconds
cli-mate -l -i 30

# Check weather in a different city
cli-mate -c "Paris"

# Show help
cli-mate -h
```

The application will start displaying the current time and updating weather and air quality information every hour when using cli-mate -l. 

## Note

This application requires an active internet connection to fetch real-time data from the OpenWeatherMap API.
