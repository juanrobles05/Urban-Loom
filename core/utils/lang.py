import json
from django.conf import settings
from pathlib import Path

LANG_PATH = Path(settings.BASE_DIR) / "resources" / "lang"

def load_translation(lang_code="en"):
    """
    Carga un archivo de traducción desde resources/lang/<lang_code>.json.
    Si no existe, hace fallback a inglés.
    """
    # Normalizar (ej: es-CO -> es)
    short_code = lang_code.split("-")[0]

    file_path = LANG_PATH / f"{short_code}.json"
    if not file_path.exists():
        file_path = LANG_PATH / "en.json"  # fallback

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}
