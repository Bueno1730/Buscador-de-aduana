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
    path('arancel/<int:arancel_id>/', views.detalle_arancel, name='detalle_arancel'),
    path('arancel/editar/<int:arancel_id>/', views.editar_arancel, name='editar_arancel'),
    path('carga-masiva/', views.carga_masiva, name='carga_masiva'),
    path('chat-ia/', views.chat_inteligente, name='chat_ia'),
    path('asistente/', views.pantalla_chat, name='pantalla_chat'), 
    path('api/chat/', views.chat_inteligente, name='chat_ia'),
    path('personal/', views.lista_usuarios, name='lista_usuarios'),
    path('personal/crear/', views.crear_usuario, name='crear_usuario'),
    path('personal/editar/<int:user_id>/', views.editar_usuario, name='editar_usuario'),
    path('personal/eliminar/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('referencias/', include('referencias.urls')),
    path('api/recurrentes/toggle/<int:arancel_id>/', views.toggle_recurrente, name='toggle_recurrente'),
    path('api/recurrentes/mis-partidas/', views.mis_recurrentes, name='mis_recurrentes'),
    path('api/recurrentes/categorias/', views.gestionar_categorias, name='gestionar_categorias'),
    path('api/recurrentes/categorias/crear/', views.crear_categoria, name='crear_categoria'),
    path('api/recurrentes/categorias/<int:categoria_id>/editar/', views.editar_categoria, name='editar_categoria'),
    path('api/recurrentes/categorias/<int:categoria_id>/eliminar/', views.eliminar_categoria, name='eliminar_categoria'),
    path('api/recurrentes/asignar-categoria/', views.asignar_categoria, name='asignar_categoria'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)