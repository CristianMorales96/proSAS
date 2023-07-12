from django.urls import path
from .views import *


urlpatterns = [
    path('', home),
    path('registrarPersonal/', registrarPersonal),
    path('edicionPersonal/<numero_documento>', edicionPersonal),
    path("editarPersonal/", editarPersonal),
    path('eliminarPersonal/<numero_documento>', eliminarPersonal),
    path('movimients/', getMoviments)
]