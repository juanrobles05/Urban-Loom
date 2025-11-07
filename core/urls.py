from django.urls import path
from .views import AboutView, weather_api, ads_api, translations_api

app_name = 'core'

urlpatterns = [
    path('about/', AboutView.as_view(), name='about'),
    path('api/weather/', weather_api, name='weather_api'),
    path('api/ads/', ads_api, name='ads_api'),
    path('api/translations/', translations_api, name='translations_api'),
]