from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from cuentas import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cuentas/', include('django.contrib.auth.urls')),
    path('', views.home, name='home'),
<<<<<<< HEAD
    path('busqueda/', views.vista_busqueda, name='busqueda'),
    path('reportes/', include('reportes.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
=======
    path('busqueda/', views.vista_busqueda, name='busqueda'), # <-- Agregamos esta línea
    path('reportes/', include('reportes.urls')),
]
>>>>>>> 45c860e9f0c9e664c4e61c94ca0a1f6104af8670
