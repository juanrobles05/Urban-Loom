from django.views.generic import TemplateView
from catalog.models import Collection

class HomeView(TemplateView):
    template_name = 'storefront/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_collections'] = Collection.objects.all()[:3]
        return context