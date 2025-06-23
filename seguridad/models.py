from django.contrib.auth.models import AbstractUser
from django.db import models
from empleado.models import Empleado  # Importar el modelo Empleado

class Usuario(AbstractUser):
    idEmpleado = models.OneToOneField(Empleado, on_delete=models.SET_NULL, null=True, blank=True)
    estaHabilitadoUsuario = models.BooleanField(default=True) 

    def __str__(self):
        return self.username