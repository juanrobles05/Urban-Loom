from django.urls import path
from .views import AboutView

app_name = 'core'

urlpatterns = [
    path('about/', AboutView.as_view(), name='about'),
]