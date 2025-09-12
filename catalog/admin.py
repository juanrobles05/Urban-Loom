from django.contrib import admin
from .models import Collection, Category, Product

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'season', 'status', 'pieces', 'is_current', 'created_at', 'image')
    list_filter = ('status', 'season', 'is_current')
    search_fields = ('name', 'description')
    list_editable = ('status', 'is_current')
    ordering = ('-created_at',)
    fields = ('name', 'season', 'description', 'image', 'pieces', 'status', 'is_current')
    readonly_fields = ('created_at',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'pieces')
    list_filter = ('status',)
    search_fields = ('name', 'description')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'collection', 'category', 'price', 'stock', 'is_active')
    list_filter = ('collection', 'category', 'is_active')
    search_fields = ('name', 'description')
    list_editable = ('price', 'stock', 'is_active')
