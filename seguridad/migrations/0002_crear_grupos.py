# Generated by Django 5.2.1 on 2025-06-15 23:06

from django.db import migrations

def crear_grupos(apps, schema_editor):
    from django.contrib.auth.models import Group
    
    # Crear los grupos si no existen
    Group.objects.get_or_create(name='Jefe')
    Group.objects.get_or_create(name='Gerente')
    Group.objects.get_or_create(name='Colaborador')

def reverse_crear_grupos(apps, schema_editor):
    from django.contrib.auth.models import Group
    
    # Eliminar los grupos (en caso de reversión de la migración)
    Group.objects.filter(name__in=['Jefe', 'Gerente', 'Colaborador']).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('seguridad', '0001_initial'),  # Asegúrate de que esta dependencia sea correcta
    ]

    operations = [
        migrations.RunPython(crear_grupos, reverse_code=reverse_crear_grupos),
    ]
