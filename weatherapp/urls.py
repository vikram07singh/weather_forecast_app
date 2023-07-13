from django.urls import path
from .views import WeatherForecastAPI

urlpatterns = [
    path('weather-forecast/', WeatherForecastAPI.as_view(), name='weather-forecast'),
]
