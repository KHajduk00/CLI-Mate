digit_map = {
    '0': [" _ ", "l l", "l_l"],
    '1': ["   ", "  l", "  l"],
    '2': [" _ ", " _l", "l_ "],
    '3': [" _ ", " _l", " _l"],
    '4': ["   ", "l_l", "  l"],
    '5': [" _ ", "l_ ", " _l"],
    '6': [" _ ", "l_ ", "l_l"],
    '7': [" _ ", "  l", "  l"],
    '8': [" _ ", "l_l", "l_l"],
    '9': [" _ ", "l_l", " _l"]
}

weather_icons = {
    "01d": "☀️",  # Clear sky (day)
    "01n": "🌙",  # Clear sky (night)
    "02d": "⛅",  # Few clouds (day)
    "02n": "🌑",  # Few clouds (night)
    "03d": "☁️",  # Scattered clouds
    "03n": "☁️",
    "04d": "☁️",  # Broken clouds
    "04n": "☁️",
    "09d": "🌧️",  # Shower rain
    "09n": "🌧️",
    "10d": "🌦️",  # Rain (day)
    "10n": "🌧️",  # Rain (night)
    "11d": "⛈️",  # Thunderstorm
    "11n": "⛈️",
    "13d": "❄️",  # Snow
    "13n": "❄️",
    "50d": "🌫️",  # Mist
    "50n": "🌫️"
}

def display_time(current_time):
    rows = ["", "", ""]
    for char in current_time:
        if char == ':':  # Handle the colon separately
            rows[0] += "   "
            rows[1] += " . "
            rows[2] += " . "
        else:
            rows[0] += digit_map[char][0] + " "
            rows[1] += digit_map[char][1] + " "
            rows[2] += digit_map[char][2] + " "
    for row in rows:
        print(row)

def get_ascii_weather_icon(icon_code):
    return weather_icons.get(icon_code, "❓")
