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
    
    # RUTAS DE RECUPERACIÓN DE CONTRASEÑA
    path('cuentas/recuperar-contrasena/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html',
        email_template_name='registration/password_reset_email.html',
        subject_template_name='registration/password_reset_subject.txt'
    ), name='password_reset'),
    
    path('cuentas/recuperar-contrasena/enviado/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),
    
    path('cuentas/restablecer/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    
    path('cuentas/restablecer/completado/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),
    # ---------------------------------------------------------
    
    path('cuentas/', include('django.contrib.auth.urls')),
    path('', views.home, name='home'),
    path('busqueda/', views.vista_busqueda, name='busqueda'),
    path('reportes/', include('reportes.urls')),
    path('agregar-arancel/', views.agregar_arancel, name='agregar_arancel'),
    path('auditoria/', views.auditoria_busquedas, name='auditoria'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)