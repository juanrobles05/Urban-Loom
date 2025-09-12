from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('collections/', views.collections_view, name='collections'),
    path('collections/<int:collection_id>/', views.collection_detail_view, name='collection_detail'),
]
