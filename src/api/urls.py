from django.urls import path
from . import views
from django.views.generic import TemplateView

# Urls in the App
urlpatterns = [
    path('weather', views.getWeather, name='weather'),
    path('weather/stats', views.getStats, name='stats'),
    path('crops', views.getCrops, name='crops')
]