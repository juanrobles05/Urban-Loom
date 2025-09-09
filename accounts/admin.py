from django.contrib import admin
from .models import User, Customer, UserProfile

admin.site.register(User)
admin.site.register(Customer)
admin.site.register(UserProfile)