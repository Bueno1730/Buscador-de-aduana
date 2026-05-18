import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Agregar 'reportes' a INSTALLED_APPS
INSTALLED_APPS = [
    # ... lo que ya tienes ...
    'reportes',
]

# Para guardar imágenes
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'reportes_errores')

# Para mensajes flash
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.SUCCESS: 'success',
    messages.ERROR: 'danger',
}