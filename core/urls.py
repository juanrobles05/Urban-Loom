from django.urls import path
from .views import AboutView, weather_api

app_name = 'core'

urlpatterns = [
    path('about/', AboutView.as_view(), name='about'),
    path('api/weather/', weather_api, name='weather_api'),
]