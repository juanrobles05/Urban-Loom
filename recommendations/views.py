from django.shortcuts import render, redirect, get_object_or_404
from .models import Wishlist, ProductRecommendation
from catalog.models import Product
from django.contrib.auth.decorators import login_required

@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    return render(request, 'recommendations/wishlist.html', {'wishlist_items': wishlist_items})

@login_required
def recommendation_view(request):
    recommendations = ProductRecommendation.objects.filter(user=request.user).select_related('product')
    return render(request, 'recommendations/recommendations.html', {'recommendations': recommendations})

@login_required
def add_to_wishlist(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, id=product_id)
        Wishlist.objects.get_or_create(user=request.user, product=product)
        return redirect(request.META.get('HTTP_REFERER', '/'))
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def remove_from_wishlist(request, product_id):
    if request.method == "POST":
        Wishlist.objects.filter(user=request.user, product_id=product_id).delete()
        return redirect('recommendations:wishlist')
    return redirect('recommendations:wishlist')
