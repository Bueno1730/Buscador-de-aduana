from django.contrib import admin
from django.urls import path, include
from cuentas import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cuentas/', include('django.contrib.auth.urls')),
    path('', views.home, name='home'),
    path('busqueda/', views.vista_busqueda, name='busqueda'), # <-- Agregamos esta línea
]