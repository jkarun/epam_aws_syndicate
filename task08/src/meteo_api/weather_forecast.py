import requests

class WeatherForecast:
    def __init__(self, latitude=52.52, longitude=13.41):
        self.base_url = "https://api.open-meteo.com/v1/forecast"
        self.latitude = latitude
        self.longitude = longitude
        self.params = {
            'latitude': self.latitude,
            'longitude': self.longitude,
            'current_weather': 'true',
            'hourly': 'temperature_2m,relative_humidity_2m,wind_speed_10m'
        }

    def get_weather(self):
        try:
            response = requests.get(self.base_url, params=self.params)
            response.raise_for_status()  # Check for HTTP request errors
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            raise e
