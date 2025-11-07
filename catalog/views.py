from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.http import JsonResponse
from .models import Collection, Product, Category

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


def shop_view(request):
    """View for displaying all products with search and filters"""
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.all()
    collections = Collection.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(collection__name__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )
    
    # Filter by category
    category_filter = request.GET.get('category', '')
    if category_filter:
        products = products.filter(category__id=category_filter)
    
    # Filter by collection
    collection_filter = request.GET.get('collection', '')
    if collection_filter:
        products = products.filter(collection__id=collection_filter)
    
    # Filter by price range
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    
    # Filter by stock availability
    stock_filter = request.GET.get('stock', '')
    if stock_filter == 'in_stock':
        products = products.filter(stock__gt=0)
    elif stock_filter == 'out_of_stock':
        products = products.filter(stock=0)
    
    # Sort functionality
    sort_by = request.GET.get('sort', 'name')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    elif sort_by == 'oldest':
        products = products.order_by('created_at')
    else:
        products = products.order_by('name')

    context = {
        'products': products,
        'categories': categories,
        'collections': collections,
        'search_query': search_query,
        'category_filter': category_filter,
        'collection_filter': collection_filter,
        'min_price': min_price,
        'max_price': max_price,
        'stock_filter': stock_filter,
        'sort_by': sort_by,
    }

    return render(request, 'shop/shop.html', context)


def products_api(request):
    """API endpoint to return products data in JSON format"""
    try:
        # Get all active products
        products = Product.objects.filter(is_active=True).select_related('category', 'collection')
        
        # Build the response data
        products_data = []
        for product in products:
            product_data = {
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'price': int(product.price),  # Convert to integer as shown in example
                'stock': product.stock,
                'is_active': product.is_active,
                'created_at': product.created_at.isoformat(),
                'image': request.build_absolute_uri(product.image.url) if product.image else None,
                'category': {
                    'id': product.category.id,
                    'name': product.category.name,
                    'status': product.category.status
                } if product.category else None,
                'collection': {
                    'id': product.collection.id,
                    'name': product.collection.name,
                    'season': product.collection.season,
                    'status': product.collection.status
                } if product.collection else None
            }
            products_data.append(product_data)
        
        # Build the final response
        response_data = {
            'success': True,
            'count': len(products_data),
            'products': products_data
        }
        
        return JsonResponse(response_data)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
