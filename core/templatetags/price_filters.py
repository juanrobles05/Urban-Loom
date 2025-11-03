from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()

@register.filter(name='format_cop')
def format_cop(value):
    """
    Formatea un precio en pesos colombianos (COP)
    Ejemplo: 150000 -> $150.000 COP
    """
    try:
        # Convertir a float y redondear
        value = float(value)
        value = round(value)

        # Formatear con separadores de miles (puntos)
        formatted = f"{value:,}".replace(',', '.')

        return f"${formatted} COP"
    except (ValueError, TypeError):
        return value

@register.filter(name='format_cop_short')
def format_cop_short(value):
    """
    Formatea un precio en pesos colombianos (COP) sin la etiqueta COP
    Ejemplo: 150000 -> $150.000
    """
    try:
        # Convertir a float y redondear
        value = float(value)
        value = round(value)

        # Formatear con separadores de miles (puntos)
        formatted = f"{value:,}".replace(',', '.')

        return f"${formatted}"
    except (ValueError, TypeError):
        return value
