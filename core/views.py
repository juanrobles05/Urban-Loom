from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

class AboutView(TemplateView):
    """Vista para mostrar la página About de Urban Loom"""
    template_name = 'core/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Información sobre Urban Loom
        context.update({
            'company_info': {
                'founded': '2025',
                'mission': 'Redefinir el streetwear urbano con diseños auténticos que reflejan la cultura de la calle moderna.',
                'vision': 'Ser la marca líder en streetwear que conecta la moda urbana con la expresión personal.',
                'values': [
                    'Autenticidad en cada diseño',
                    'Calidad premium en materiales',
                    'Conexión con la cultura urbana',
                    'Innovación constante',
                    'Respeto por la comunidad',
                    'Sostenibilidad y responsabilidad'
                ]
            },
        })
        
        return context
