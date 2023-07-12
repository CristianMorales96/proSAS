from django.db import models

# Create your models here.
class Staff(models.Model):
    id = models.AutoField(primary_key=True)
    nombres = models.CharField(max_length=30)
    apellidos = models.CharField(max_length=30)
    tipo_documento = models.CharField(max_length=50)
    numero_documento = models.CharField(max_length=50)

    def __str__(self):
        texto = "{0} {1}"
        return texto.format(self.nombres, self.apellidos)

    class Meta:
        db_table = "empleados_staff"



class Autorization(models.Model):
    id = models.AutoField(primary_key=True)
    hora_inicio = models.CharField(max_length=50)
    hora_final = models.CharField(max_length=50)
    fecha =  models.CharField(max_length=50)
    id_empleado = models.ForeignKey(Staff, on_delete=models.CASCADE)

    def __str__(self):
        texto = "{0}"
        return texto.format(self.id_empleado)

    class Meta:
        db_table = "empleados_autorization"

class Moviment(models.Model):
    id = models.AutoField(primary_key=True)
    fecha_entrada = models.CharField(max_length=50)
    fecha_salida = models.CharField(max_length=50)
    hora_entrada = models.CharField(max_length=50)
    hora_salida =  models.CharField(max_length=50)
    sentido = models.CharField(max_length=50, null="ENTRADA")
    id_empleado = models.ForeignKey(Staff, on_delete=models.CASCADE)

    def __str__(self):
        texto = "{0}"
        return texto.format(self.id_empleado)

    class Meta:
        db_table = "empleados_moviments"