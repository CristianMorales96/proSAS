from django.urls import path
from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('registrarPersonal/', registrarPersonal, name='registrarPersonal'),
    path('edicionPersonal/<numero_documento>', edicionPersonal, name='edicionPersonal'),
    path('editarPersonal/', editarPersonal, name='editarPersonal'),
    path('eliminarPersonal/<numero_documento>', eliminarPersonal, name='eliminarPersonal'),
    path('movimients/', getMoviments, name='movimientosPersonal'),
    path('autorization/', autorizationPersonal, name='autorizacionPersonal'),
    path('registrarAutorization/', registrarAutorization, name='registrarAutorizacion'),
    path('edicionAutorizacion/<id_empleado>', edicionAutorizacion)
]