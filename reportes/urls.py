from django.urls import path
from . import views

app_name = 'reportes'

urlpatterns = [
    path('reportar/', views.reportar_error, name='reportar'),
    path('confirmacion/<int:reporte_id>/', views.confirmacion_reporte, name='confirmacion'),
    path('mis-reportes/', views.mis_reportes, name='mis_reportes'),
    path('admin/reportes/', views.lista_reportes_admin, name='admin_lista'),
    path('admin/reportes/<int:reporte_id>/', views.detalle_reporte_admin, name='admin_detalle'),
]