from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse
import requests
import logging

# Create your views here.

logger = logging.getLogger(__name__)

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


def weather_api(request):
    """API endpoint to get weather data based on location"""
    try:
        # Default coordinates for Medellín, Colombia
        default_lat = 6.2442
        default_lng = -75.5812
        
        # Get coordinates from request parameters
        latitude = request.GET.get('lat', default_lat)
        longitude = request.GET.get('lng', default_lng)
        
        # Validate coordinates
        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except (ValueError, TypeError):
            latitude = default_lat
            longitude = default_lng
        
        # Open-Meteo API URL
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true&timezone=America/Bogota"
        
        # Make request to weather API
        response = requests.get(weather_url, timeout=10)
        response.raise_for_status()
        
        weather_data = response.json()
        
        # Extract relevant weather information
        current_weather = weather_data.get('current_weather', {})
        
        # Map weather codes to descriptions (WMO Weather interpretation codes)
        weather_descriptions = {
            0: "Despejado",
            1: "Mayormente despejado", 
            2: "Parcialmente nublado",
            3: "Nublado",
            45: "Niebla",
            48: "Niebla con escarcha",
            51: "Llovizna ligera",
            53: "Llovizna moderada", 
            55: "Llovizna densa",
            56: "Llovizna helada ligera",
            57: "Llovizna helada densa",
            61: "Lluvia ligera",
            63: "Lluvia moderada",
            65: "Lluvia fuerte",
            66: "Lluvia helada ligera",
            67: "Lluvia helada fuerte",
            71: "Nieve ligera",
            73: "Nieve moderada",
            75: "Nieve fuerte",
            77: "Granizo",
            80: "Aguaceros ligeros",
            81: "Aguaceros moderados",
            82: "Aguaceros fuertes",
            85: "Nevadas ligeras",
            86: "Nevadas fuertes",
            95: "Tormenta",
            96: "Tormenta con granizo ligero",
            99: "Tormenta con granizo fuerte"
        }
        
        weather_code = current_weather.get('weathercode', 0)
        weather_description = weather_descriptions.get(weather_code, "Condición desconocida")
        
        # Format response
        weather_response = {
            'success': True,
            'location': {
                'latitude': latitude,
                'longitude': longitude,
                'city': 'Medellín' if latitude == default_lat and longitude == default_lng else 'Ubicación actual'
            },
            'weather': {
                'temperature': current_weather.get('temperature'),
                'temperature_unit': weather_data.get('current_weather_units', {}).get('temperature', '°C'),
                'windspeed': current_weather.get('windspeed'),
                'windspeed_unit': weather_data.get('current_weather_units', {}).get('windspeed', 'km/h'),
                'winddirection': current_weather.get('winddirection'),
                'weathercode': weather_code,
                'description': weather_description,
                'time': current_weather.get('time'),
                'is_day': current_weather.get('is_day', 1) == 1
            }
        }
        
        return JsonResponse(weather_response)
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching weather data: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'Error al obtener datos del clima'
        }, status=500)
        
    except Exception as e:
        logger.error(f"Unexpected error in weather API: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'Error interno del servidor'
        }, status=500)


def ads_api(request):
    """API endpoint to get advertising data from tech company"""
    try:
        # TODO: Replace with actual endpoint from tech company
        tech_company_url = "https://api.techstore.example.com/products"
        
        try:
            # Try to fetch from external API
            response = requests.get(tech_company_url, timeout=5)
            response.raise_for_status()
            
            # Parse the actual response from tech company
            data = response.json()
            
            # Assuming the tech company returns an array of products
            # Adjust this parsing based on their actual API response format
            if isinstance(data, list) and len(data) > 0:
                # Take up to 3 products
                products = data[:3] if len(data) >= 3 else data
                
                return JsonResponse({
                    'success': True,
                    'ad_products': products,
                    'company': 'TechStore Pro'
                })
            else:
                # No products available
                return JsonResponse({
                    'success': False,
                    'error': 'No hay productos disponibles'
                })
            
        except requests.exceptions.RequestException:
            # External API is not available or failed
            return JsonResponse({
                'success': False,
                'error': 'Servicio de publicidad no disponible'
            })
        
    except Exception as e:
        logger.error(f"Error in ads API: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'Error al cargar publicidad'
        }, status=500)


def translations_api(request):
    """API endpoint to get translations for JavaScript"""
    from .utils.lang import load_translation
    
    # Get language from request
    lang = getattr(request, "LANGUAGE_CODE", "es")
    if not lang:
        lang = "es"
    
    # Load translations
    t = load_translation(lang)
    
    # Return only needed translations for ads widget
    ads_translations = {
        'ADS_TITLE': t.get('ADS_TITLE', 'Publicidad'),
        'ADS_VIEW_DETAILS': t.get('ADS_VIEW_DETAILS', 'Ver detalles'),
        'ADS_NO_DATA': t.get('ADS_NO_DATA', 'Publicidad no disponible')
    }
    
    return JsonResponse({
        'success': True,
        'translations': ads_translations,
        'lang': lang.split("-")[0] if "-" in lang else lang
    })
