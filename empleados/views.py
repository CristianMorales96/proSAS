from django.shortcuts import redirect, render
import json
from .models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.http import HttpResponseForbidden
from datetime import datetime


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

@csrf_exempt #consultaro desde cualquier cliente
def getMoviments(request):
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
        try:
            encontrar = Staff.objects.get(id=id_empleado)
        except:
            return JsonResponse({"data": "Empleado no encontrado"})
        try:
            autorizacion = Autorization.objects.filter(id_empleado=id_empleado).values()
            errores = ""
            encontrado = 0
            for item in autorizacion:
                if fecha_entrada.count("-") == 2:
                    encontrado += 1
                elif fecha_entrada.count("-") != 2:
                    errores += "Formato de fecha de entrada no valido. Ejemplo: 01-01-2023"
                    break
                if fecha_salida.count("-") == 2:
                    encontrado += 1
                elif fecha_salida.count("-") != 2:
                    errores += "Formato de fecha de salida no valido. Ejemplo: 01-01-2023"
                    break
                if item["fecha"] == fecha_entrada:
                    encontrado += 1
                elif item["fecha"] != fecha_entrada:
                    errores += "El usuario no se encuentra autorizado para entrar esta fecha"
                    break
                if item["fecha"] == fecha_salida:
                    encontrado += 1
                elif item["fecha"] != fecha_salida:
                    errores += "El usuario no se encuentra autorizado para salir esta fecha"
                    break
                if item["hora_inicio"] <= hora_entrada:
                    encontrado += 1
                elif item["hora_inicio"] > hora_entrada:
                    errores += "El usuario no se encuentra autorizado para entrar a esta hora"
                    break
                if item["hora_final"] >= hora_salida:
                    encontrado += 1
                elif item["hora_final"] < hora_salida:
                    errores += "El usuario no se encuentra autorizado para salir a esta hora"
                    break
                if hora_entrada <= "23:59":
                    encontrado += 1
                elif hora_entrada > "23:59":
                    errores += "La hora no es valida"
                    break
                if hora_salida <= "23:59":
                    encontrado += 1
                elif hora_salida > "23:59":
                    errores += "La hora no es valida"
                    break
                if hora_entrada.count(":") == 1:
                    encontrado += 1
                elif hora_entrada.count(":") != 1:
                    errores += "La hora de entrada no es valida. Ejemplo: 07:00 y debe ser en hora militar"
                    break
                if hora_salida.count(":") == 1:
                    encontrado += 1
                elif hora_salida.count(":") != 1:
                    errores += "La hora de salida no es valida. Ejemplo: 07:00 y debe ser en hora militar"
                    break
                if sentido == "ENTRADA" or sentido == "SALIDA":
                    encontrado += 1
                elif sentido != "ENTRADA" and sentido != "SALIDA":
                    errores += "El sentido debe ser ENTRADA O SALIDA"
                    break

        except Exception as e:
            return JsonResponse({"data": "El empleado no se encuentra autorizado"})
        if errores != "" and encontrado != 12:
            return JsonResponse({"data": errores})
        moviments = Moviment.objects.create(fecha_entrada = fecha_entrada, fecha_salida = fecha_salida, hora_entrada = hora_entrada,
                                            hora_salida = hora_salida, sentido = sentido, id_empleado = encontrar)
        return JsonResponse({"data": "created"})
    return HttpResponseForbidden()



def autorizationPersonal(request):
    autorizationlist = Autorization.objects.all()
    buscar_empleado = Staff.objects.all()
    return render(request, "autorization.html", {"Autorization": autorizationlist,
                                                 "Staff": buscar_empleado})




def registrarAutorization(request):
    hora_inicio = request.POST["entradaAutorization"]
    hora_final = request.POST["salidaAutorization"]
    fecha = request.POST["trip-start"]
    id_empleado = request.POST["txtidEmpleado"]
    buscar = Staff.objects.get(id=id_empleado)
    fecha = datetime.strptime(fecha, "%Y-%m-%d")
    fecha_formateada = fecha.strftime("%d-%m-%Y").split(" ")[0]
    print(fecha_formateada)

    autorization = Autorization.objects.create(hora_inicio = hora_inicio, hora_final = hora_final,
                                               fecha = fecha_formateada, id_empleado = buscar)
    return redirect('/autorization/')


def edicionAutorizacion(request, id):
    print("probando")
    autorization = Autorization.objects.get(id=id)
    print(autorization)
    return render(request, "edicionAutorizacion.html", {"autorization": autorization})

def editarAutorizacion(request):
    hora_inicio = request.POST["txtnomhoraInicio"]
    hora_final = request.POST["txthoraFinal"]
    fecha = request.POST["txtfecha"]
    id_empleado = request.POST["txtidEmpleado"]
    id = request.POST["id"]
    staff = Staff.objects.get(id=id_empleado)

    autorization = Autorization.objects.get(id=id)
    autorization.hora_inicio = hora_inicio
    autorization.hora_final = hora_final
    autorization.fecha = fecha
    autorization.id_empleado = staff
    autorization.save()

    return redirect('/autorization/')



def eliminarAutorizacion(request, id):
    autorization = Autorization.objects.get(id=id)
    autorization.delete()
    return redirect('/autorization/')

