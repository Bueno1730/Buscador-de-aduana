from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from cuentas import views
from django.contrib.auth import views as auth_views
from cuentas.forms import CustomLoginForm

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('cuentas/login/', auth_views.LoginView.as_view(
        template_name='registration/login.html',
        authentication_form=CustomLoginForm
    ), name='login'),
    
    path('cuentas/', include('django.contrib.auth.urls')),
    path('', views.home, name='home'),
    path('busqueda/', views.vista_busqueda, name='busqueda'),
    path('reportes/', include('reportes.urls')),
    path('agregar-arancel/', views.agregar_arancel, name='agregar_arancel'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)