from django.shortcuts import render, get_object_or_404
from .models import Collection, Product

def collections_view(request):
    """View for displaying all collections page"""

    current_collection = Collection.objects.filter(is_current=True).first()

    all_collections = Collection.objects.all()

    latest_collection = all_collections.first()

    context = {
        'current_collection': current_collection,
        'all_collections': all_collections,
        'latest_collection': latest_collection,
    }

    return render(request, 'catalog/collections.html', context)


def collection_detail_view(request, collection_id):
    """View for displaying individual collection details"""
    collection = get_object_or_404(Collection, id=collection_id)
    products = collection.products.filter(is_active=True)

    context = {
        'collection': collection,
        'products': products,
    }

    return render(request, 'catalog/collection_detail.html', context)


def product_detail_view(request, product_id):
    """View to display individual product details"""
    product = get_object_or_404(Product, id=product_id)

    context = {
        'product': product,
    }

    return render(request, 'catalog/product_detail.html', context)
