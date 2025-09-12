from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('collections/', views.collections_view, name='collections'),
    path('collections/<int:collection_id>/', views.collection_detail_view, name='collection_detail'),
    path('products/<int:product_id>/', views.product_detail_view, name='product_detail'),
]
