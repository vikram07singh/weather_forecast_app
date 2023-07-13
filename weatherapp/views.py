from rest_framework import generics
from .models import WeatherForecast
from .serializers import WeatherForecastSerializer
from datetime import datetime, timedelta
import requests
import json

API_KEY = '71f6779186cc32448b4c412eea65b982'
TIME_SENSITIVITY = timedelta(minutes=10)

class WeatherForecastAPI(generics.RetrieveAPIView):
    serializer_class = WeatherForecastSerializer
    template_name = 'weatherapp/weather_app.html'
    def get_object(self):
        lat = self.request.query_params.get('lat')
        lon = self.request.query_params.get('lon')
        detailing_type = self.request.query_params.get('detailing_type')

        # Check if the data is available in the local database
        try:
            weather_forecast = WeatherForecast.objects.filter(latitude=lat, longitude=lon, detailing_type=detailing_type).latest('timestamp')
            timestamp_difference = datetime.now().replace(tzinfo=None) - weather_forecast.timestamp.replace(tzinfo=None)

            # Check if the data is still relevant
            if timestamp_difference < TIME_SENSITIVITY:
                return weather_forecast

        except WeatherForecast.DoesNotExist:
            pass

        # Request data from OpenWeatherMap API
        api_url = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=current,minutely&appid={API_KEY}'
        response = requests.get(api_url)
        data = json.loads(response.text)

        # Save the data to the local database
        weather_forecast = WeatherForecast.objects.create(
            latitude=lat,
            longitude=lon,
            detailing_type=detailing_type,
            data=data
        )
        context = {
        'weather': weather_forecast
    }

        return weather_forecast
