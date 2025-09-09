from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import set_language
from storefront import views

urlpatterns = [
    path("set-language/", set_language, name="set_language"),
    path('', views.HomeView.as_view(), name="home"),
]