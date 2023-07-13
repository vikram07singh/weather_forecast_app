from django.db import models

class WeatherForecast(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    detailing_type = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
    data = models.JSONField()
