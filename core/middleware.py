from django.utils.translation import activate
from django.conf import settings


class LanguageMiddleware:
    """
    Middleware para gestionar el idioma de la aplicación.
    Busca el idioma en:
    1. Parámetro GET (?lang=es o ?lang=en)
    2. Cookie 'user_language'
    3. Accept-Language header del navegador
    4. Valor por defecto de settings.LANGUAGE_CODE
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. Prioridad: parámetro GET
        lang = request.GET.get('lang')

        # 2. Si no hay parámetro, revisar cookie
        if not lang:
            lang = request.COOKIES.get('user_language')

        # 3. Si no hay cookie, revisar Accept-Language
        if not lang and request.META.get('HTTP_ACCEPT_LANGUAGE'):
            accept_lang = request.META['HTTP_ACCEPT_LANGUAGE']
            # Tomar el primer idioma del header
            lang = accept_lang.split(',')[0].split('-')[0].strip()

        # 4. Fallback a español por defecto
        if not lang or lang not in ['es', 'en']:
            lang = settings.LANGUAGE_CODE.split('-')[0]

        # Normalizar el código (eliminar variantes regionales)
        lang_code = lang.split('-')[0]

        # Activar el idioma para Django
        activate(lang_code)

        # Guardar en el request para uso posterior
        request.LANGUAGE_CODE = lang_code

        response = self.get_response(request)

        # Si vino un parámetro GET, guardar en cookie
        if request.GET.get('lang'):
            response.set_cookie('user_language', lang_code, max_age=365*24*60*60)

        return response
