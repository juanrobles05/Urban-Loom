from django.conf import settings
from django.utils.translation import get_language
from .utils.lang import load_translation

def translations(request):
    """
    Context processor que inyecta las traducciones en todas las vistas.
    """
    # Idioma activo por middleware o por configuración
    lang = getattr(request, "LANGUAGE_CODE", None) or get_language()

    # Si no hay idioma, usar el default del proyecto
    if not lang:
        lang = settings.LANGUAGE_CODE  # ej: "es-CO"

    # Cargar traducciones desde resources/lang
    t = load_translation(lang)

    return {
        "t": t,  # diccionario con los textos
        "LANG": lang.split("-")[0],  # útil para <html lang="{{ LANG }}">
    }
