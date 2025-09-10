from django.urls import path
from .views import (
    register_user, login_user, logout_user, profile_view,
    edit_profile,
    add_shipping_address, list_shipping_addresses,
    edit_shipping_address, delete_shipping_address
)

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('addresses/add/', add_shipping_address, name='add_shipping_address'),
    path('addresses/', list_shipping_addresses, name='list_shipping_addresses'),
    path('addresses/<int:address_id>/edit/', edit_shipping_address, name='edit_shipping_address'),
    path('addresses/<int:address_id>/delete/', delete_shipping_address, name='delete_shipping_address'),
]