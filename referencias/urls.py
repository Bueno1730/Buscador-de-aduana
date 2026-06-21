from django.urls import path
from . import views

app_name = 'referencias'

urlpatterns = [
    path('', views.lista_referencias, name='lista'),
    path('<int:referencia_id>/', views.detalle_referencia, name='detalle'),
]
