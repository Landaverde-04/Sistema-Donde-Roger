from django.core.management.base import BaseCommand
from django.db import connection
from django.apps import apps

class Command(BaseCommand):
    help = "Para los indices de las tablas, que ya no se den errores con los backups"
    
    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            for model in apps.get_models():
                table = model._meta.db_table
                pk_field = model._meta.pk.column
                pk_field_object = model._meta.pk
                
                #Verifica que la PK sea numerica
                if not hasattr(pk_field_object,'get_internal_type'):
                    continue
                pk_type = pk_field_object.get_internal_type()
                if pk_type not in ('AutoField', 'BigAutoField', 'SmallAutoField', 'IntegerField', 'BigIntegerField'):
                    self.stdout.write(f"La tabla: {table} no tiene PK numerica")
                    continue
                
                
                self.stdout.write(f"Reseteando secuencias de {table}")
                
                try:
                    cursor.execute(f"""SELECT setval(pg_get_serial_sequence('"{table}"','{pk_field}'), COALESCE((SELECT MAX("{pk_field}") FROM "{table}"), 1), (SELECT COUNT (*) > 0 FROM "{table}"));""")
                except Exception as e:
                    self.stdout.write(f"Error al resetear la secuencia de {table}: {e}")
                    continue
            self.stdout.write(self.style.SUCCESS("Se ajustaron las secuencias de las tablas"))
