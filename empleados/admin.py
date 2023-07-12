from django.contrib import admin
from empleados.models import Autorization, Moviment, Staff

# Register your models here.
admin.site.register(Staff)
admin.site.register(Autorization)
admin.site.register(Moviment)