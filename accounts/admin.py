from django.contrib import admin
from .models import User, Customer, UserProfile, ShippingAddress

admin.site.register(User)
admin.site.register(Customer)
admin.site.register(UserProfile)
admin.site.register(ShippingAddress)