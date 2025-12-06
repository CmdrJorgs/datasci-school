""" ============================================
Title: Final Project - Weather Application
Author: David Jorgensen
Course: DSC 510
Date: 23 November 2025
Description: Application to interact with OpenWeatherMap API
             to obtain and display weather data for US locations.
=========================================== """

import requests
import os

# API Key for OpenWeatherMap
API_KEY = "71ddeb856877737266bf4bdb97119a92"
GEO_API_URL = "https://api.openweathermap.org/geo/1.0/"
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_temperature_unit():
    """Prompt user to select temperature unit (Fahrenheit or Celsius)."""
    while True:
        print("\nSelect temperature unit:")
        print("1. Fahrenheit")
        print("2. Celsius")
        unit_choice = input("Enter your choice (1 or 2): ").strip()
        
        if unit_choice == "1":
            return "imperial", "°F"
        elif unit_choice == "2":
            return "metric", "°C"
        else:
            print("Invalid choice. Please enter 1 or 2.")


def validate_zip_code(zip_code_input):
    """Validate that input is a valid US zip code."""
    zip_code_input = zip_code_input.strip()
    if not zip_code_input.isdigit() or len(zip_code_input) != 5:
        print("Invalid zip code. Please enter a 5-digit US zip code.")
        return None
    return zip_code_input


def validate_city_state(city_input, state_input):
    """Validate that city and state inputs are non-empty strings."""
    city_input = city_input.strip()
    state_input = state_input.strip()
    
    if not city_input or not city_input.replace(" ", "").isalpha():
        print("Invalid city name. Please enter a valid city name.")
        return None, None
    
    if not state_input or len(state_input) != 2 or not state_input.isalpha():
        print("Invalid state. Please enter a 2-letter state abbreviation.")
        return None, None
    
    return city_input, state_input.upper()


def get_geolocation(location_query, query_type):
    """
    Retrieve latitude and longitude for a given location.
    location_query can be a zip code or "city,state" format.
    Returns tuple of (latitude, longitude, location_name) or (None, None, None) on failure.
    """
    try:
        if query_type == "zip":
            parameters = {
            "zip": location_query,
            "appid": API_KEY
            }
        elif query_type == "direct":
            parameters = {
            "q": location_query,
            "limit": 1,
            "appid": API_KEY
            }
        else:
            print("Invalid query type for geolocation.")
            return None, None, None
        
        api_address = GEO_API_URL + query_type
        response = requests.get(api_address, params=parameters)
        response.raise_for_status()
        
        data = response.json()

        if isinstance(data, list):
            if not data:
                print(f"Location not found: {location_query}")
                return None, None, None
            data = data[0]
        if not data:
            print(f"Location not found: {location_query}")
            return None, None, None
        
        latitude = data.get('lat', '')
        longitude = data.get('lon', '')
        location_name = f"{data.get('name', '')}, {data.get('state', '')} {data.get('country', '')}"
        
        return latitude, longitude, location_name
    
    except requests.exceptions.RequestException as error:
        print(f"Error connecting to geolocation service: {error}. Perhaps your location does not exist?")
        return None, None, None


def get_weather_data(latitude, longitude, temperature_unit):
    """
    Retrieve weather data for given latitude and longitude.
    Returns weather data dictionary or None on failure.
    """
    try:
        parameters = {
            "lat": latitude,
            "lon": longitude,
            "units": temperature_unit,
            "appid": API_KEY
        }
        
        response = requests.get(WEATHER_API_URL, params=parameters)
        response.raise_for_status()
        
        weather_data = response.json()
        return weather_data
    
    except requests.exceptions.RequestException as error:
        print(f"Error connecting to weather service: {error}")
        return None


class WeatherReport:
    """Encapsulates weather data and display formatting."""
    def __init__(self, weather_data, location_name, temperature_symbol):
        """Initialize WeatherReport with weather data and location information."""
        self.weather_data = weather_data
        self.location_name = location_name
        self.temperature_symbol = temperature_symbol
        self._extract_weather_info()
    
    def _extract_weather_info(self):
        """Extract weather information from API response."""
        main_info = self.weather_data["main"]
        weather_info = self.weather_data["weather"][0]
        clouds_info = self.weather_data.get("clouds", {})
        
        self.current_temperature = main_info["temp"]
        self.high_temperature = main_info["temp_max"]
        self.low_temperature = main_info["temp_min"]
        self.pressure = main_info["pressure"]
        self.humidity = main_info["humidity"]
        self.cloud_coverage = clouds_info.get("all", 0)
        self.description = weather_info["description"].capitalize()
        self.weather_main = weather_info["main"]
    
    def _get_weather_icon(self):
        """Return ASCII art icon based on weather condition."""
        weather_type = self.weather_main.lower()
        
        if "clear" in weather_type or "sunny" in weather_type:
            return """
    \\  /
  _\\ /_
    / \\
   /   \\
"""
        elif "cloud" in weather_type:
            return """
     _____
    /     \\
   | O   O |
    \\ --- /
"""
        elif "rain" in weather_type:
            return """
     _____
    /     \\
   |  ◡◡◡  |
    \\ | | /
     \\|_|/
"""
        elif "thunder" in weather_type or "storm" in weather_type:
            return """
     _____
    /     \\
   | ⚡ ⚡ |
    \\ | | /
     \\|_|/
"""
        elif "snow" in weather_type:
            return """
     _____
    /     \\
   | * * * |
    \\ * * /
     \\*/
"""
        elif "mist" in weather_type or "fog" in weather_type:
            return """
   ~~~~~~
   ~~~~~~
   ~~~
"""
        else:
            return """
     ___
    /   \\
   |  ?  |
    \\___ /
"""
    
    def display(self):
        """Display weather information in a readable format."""
        weather_icon = self._get_weather_icon()
        
        print("\n" + "=" * 70)
        print(f"Weather Forecast for: {self.location_name}")
        print("=" * 70)
        
        print(weather_icon)
        print(f"Weather Condition: {self.description}")
        print(f"Current Temperature: {self.current_temperature}{self.temperature_symbol}")
        print(f"High Temperature: {self.high_temperature}{self.temperature_symbol}")
        print(f"Low Temperature: {self.low_temperature}{self.temperature_symbol}")
        print(f"Pressure: {self.pressure} hPa")
        print(f"Humidity: {self.humidity}%")
        print(f"Cloud Coverage: {self.cloud_coverage}%")
        
        print("=" * 70)


def display_weather(weather_data, location_name, temperature_unit_symbol):
    """Display weather information in a readable format."""
    weather_report = WeatherReport(weather_data, location_name, temperature_unit_symbol)
    weather_report.display()


def lookup_weather_by_zip_code(temperature_unit, temperature_symbol):
    """Handle weather lookup by zip code."""
    zip_code = input("Enter a 5-digit US zip code: ").strip()
    
    validated_zip = validate_zip_code(zip_code)
    if validated_zip is None:
        return
    
    # Get geolocation data
    latitude, longitude, location_name = get_geolocation(validated_zip, "zip")
    if latitude is None or longitude is None:
        return
    
    # Get weather data
    weather_data = get_weather_data(latitude, longitude, temperature_unit)
    if weather_data is None:
        return
    
    # Display weather information
    display_weather(weather_data, location_name, temperature_symbol)


def lookup_weather_by_city_state(temperature_unit, temperature_symbol):
    """Handle weather lookup by city and state."""
    city = input("Enter city name: ").strip()
    state = input("Enter state abbreviation (e.g., CA, TX, NY): ").strip()
    
    validated_city, validated_state = validate_city_state(city, state)
    if validated_city is None or validated_state is None:
        return
    
    # Format location query for geolocation API
    location_query = f"{validated_city},{validated_state},US"
    
    # Get geolocation data
    latitude, longitude, location_name = get_geolocation(location_query, "direct")
    if latitude is None or longitude is None:
        return
    
    # Get weather data
    weather_data = get_weather_data(latitude, longitude, temperature_unit)
    if weather_data is None:
        return
    
    # Display weather information
    display_weather(weather_data, location_name, temperature_symbol)


def main():
    """Main function to run the weather application."""
    # Clear the console
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("=" * 70)
    print("Welcome to the Weather Lookup Application!")
    print("=" * 70)
    
    # Get user's preferred temperature unit
    temperature_unit, temperature_symbol = get_temperature_unit()
    
    # Main loop to allow multiple lookups
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=" * 70)
        print("Weather Lookup Options")
        print("=" * 70)
        print("1. Lookup weather by zip code")
        print("2. Lookup weather by city and state")
        print("3. Exit")
        print("=" * 70)
        
        user_choice = input("Enter your choice (1, 2, or 3): ").strip()
        
        if user_choice == "1":
            lookup_weather_by_zip_code(temperature_unit, temperature_symbol)
        elif user_choice == "2":
            lookup_weather_by_city_state(temperature_unit, temperature_symbol)
        elif user_choice == "3":
            print("\nThank you for using the Weather Lookup Application!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
            continue
        
        # Ask user if they want to perform another lookup
        another_lookup = input("\nWould you like to perform another lookup? (y/n): ").strip().lower()
        if another_lookup != 'y':
            print("\nThank you for using the Weather Lookup Application!")
            exit()


# Run the main function
if __name__ == "__main__":
    main()
