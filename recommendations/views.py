from django.shortcuts import render
from .models import Wishlist, ProductRecommendation
from django.contrib.auth.decorators import login_required

@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    return render(request, 'recommendations/wishlist.html', {'wishlist_items': wishlist_items})

@login_required
def recommendation_view(request):
    recommendations = ProductRecommendation.objects.filter(user=request.user).select_related('product')
    return render(request, 'recommendations/recommendations.html', {'recommendations': recommendations})
