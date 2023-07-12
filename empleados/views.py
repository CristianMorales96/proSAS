from django.shortcuts import redirect, render
import json
from .models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.http import HttpResponseForbidden


def home(request):
    stafflist = Staff.objects.all()
    return render(request, "crud.html", {"Staff": stafflist})


def registrarPersonal(request):
    nombres = request.POST["txtnombrePersonal"]
    apellidos = request.POST["txtapellidoPersonal"]
    tipo_documento = request.POST["txttipoDocumentoPersonal"]
    numero_documento = request.POST["txtnumeroDocumentoPersonal"]

    staff = Staff.objects.create(nombres = nombres, apellidos = apellidos, tipo_documento = tipo_documento, numero_documento = numero_documento)
    return redirect('/')

def eliminarPersonal(request, numero_documento):
    personal = Staff.objects.get(numero_documento=numero_documento)
    personal.delete()
    return redirect('/')

def edicionPersonal(request, numero_documento):
    personal = Staff.objects.get(numero_documento=numero_documento)
    return render(request, "edicionPersonal.html", {"personal": personal})

def editarPersonal(request):
    nombres = request.POST["txtnombrePersonal"]
    apellidos = request.POST["txtapellidoPersonal"]
    tipo_documento = request.POST["txttipoDocumentoPersonal"]
    numero_documento = request.POST["txtnumeroDocumentoPersonal"]
    id=request.POST["id"]

    personal = Staff.objects.get(id=id)
    personal.nombres = nombres
    personal.apellidos = apellidos
    personal.tipo_documento = tipo_documento
    personal.numero_documento = numero_documento
    personal.save()

    return redirect('/')

@csrf_exempt
def getMoviments(request):
    print(request.method)
    if request.method == "GET":
        moviments = Moviment.objects.all()
        data = serializers.serialize('json', moviments)
        return JsonResponse({"data": json.loads(data)})

    if request.method == "POST":
        prueba = (json.loads(request.body.decode('utf-8')))
        try:
            fecha_entrada = prueba["fecha_entrada"]
            fecha_salida = prueba["fecha_salida"]
            hora_entrada = prueba["hora_entrada"]
            hora_salida = prueba["hora_salida"]
            sentido = prueba["sentido"]
            id_empleado = prueba["id_empleado"]
        except:
            return JsonResponse({"data": "fecha_entrada, fecha_salida, hora_entrada, hora_salida, sentido, id_empleado son obligatorios"})
        if fecha_entrada == "":
            return JsonResponse({"data": "fecha de entrada no puede ser vacia"})
        try:
            encontrar = Staff.objects.get(id=id_empleado)
        except:
            return JsonResponse({"data": "Empleado no encontrado"})
        try:
            autorizacion = Autorization.objects.get(id_empleado=id_empleado)
        except:
            return JsonResponse({"data": "El empleado no se encuentra autorizado"})
        if autorizacion.fecha != fecha_entrada:
            return JsonResponse({"data": "El usuario no se encuentra autorizado para ingresar esta fecha"})
        if autorizacion.fecha != fecha_salida:
            return JsonResponse({"data": "El usuario no se encuentra autorizado para salir esta fecha"})
        if autorizacion.hora_inicio > hora_entrada:
            return JsonResponse({"data": "El usuario no se encuentra autorizado para entrar a esta hora"})
        if autorizacion.hora_final < hora_salida:
            return JsonResponse({"data": "El usuario no se encuentra autorizado para salir a esta hora"})
        if hora_entrada > "23:59":
            return JsonResponse({"data": "La hora no es valida"})
        if hora_salida > "23:59":
            return JsonResponse({"data": "La hora no es valida"})
        if sentido != "ENTRADA" and sentido != "SALIDA":
            return JsonResponse({"data": "El sentido debe ser ENTRADA O SALIDA"})
        moviments = Moviment.objects.create(fecha_entrada = fecha_entrada, fecha_salida = fecha_salida, hora_entrada = hora_entrada,
                                            hora_salida = hora_salida, sentido = sentido, id_empleado = encontrar)
        return JsonResponse({"data": "created"})
    return HttpResponseForbidden()


