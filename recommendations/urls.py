from django.urls import path
from . import views

urlpatterns = [
    path('', views.recommendation_view, name='recommendations'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
]
