from django.db import models

# Create model for Weather
class Weather(models.Model):
    Date = models.TextField()
    Maxtemp = models.FloatField()
    Mintemp = models.FloatField()
    Precipitation = models.FloatField()
    Station_id = models.TextField()

    class Meta:
        db_table = "weather_data"

# Create model for stats
class Stats(models.Model):
    Year = models.TextField()
    Station_id = models.TextField()
    Average_Maxtemp = models.FloatField()
    Average_Mintemp = models.FloatField()
    Sum_Precipitation = models.FloatField()

    class Meta:
        db_table = 'weather_stats'

# Create model for crop yields
class Crops(models.Model):
    Date = models.TextField()
    Yield = models.FloatField()

    class Meta:
        db_table = 'crop_data'