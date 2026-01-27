# Generated manually for initial catalog data

from django.db import migrations

def add_catalog_data(apps, schema_editor):
    TipoPedidoCliente = apps.get_model('Gestion_Pedidos_Clientes', 'TipoPedidoCliente')
    EstadoPedidoCliente = apps.get_model('Gestion_Pedidos_Clientes', 'EstadoPedidoCliente')
    
    # Crear tipos de pedido si no existen
    tipos_pedido = [
        {'idTipoPedido': 1, 'nombreTipoPedido': 'En restaurante'},
        {'idTipoPedido': 2, 'nombreTipoPedido': 'Cliente recogerá'},
        {'idTipoPedido': 3, 'nombreTipoPedido': 'A domicilio'},
    ]
    
    for tipo_data in tipos_pedido:
        TipoPedidoCliente.objects.get_or_create(
            idTipoPedido=tipo_data['idTipoPedido'],
            defaults={'nombreTipoPedido': tipo_data['nombreTipoPedido']}
        )
    
    # Crear estados de pedido si no existen
    estados_pedido = [
        {'idEstado': 1, 'nombreEstado': 'Pendiente'},
        {'idEstado': 2, 'nombreEstado': 'En preparación'},
        {'idEstado': 3, 'nombreEstado': 'Listo para recoger'},
        {'idEstado': 4, 'nombreEstado': 'En camino'},
        {'idEstado': 5, 'nombreEstado': 'Entregado'},
        {'idEstado': 6, 'nombreEstado': 'Cancelado'},
    ]
    
    for estado_data in estados_pedido:
        EstadoPedidoCliente.objects.get_or_create(
            idEstado=estado_data['idEstado'],
            defaults={'nombreEstado': estado_data['nombreEstado']}
        )

def remove_catalog_data(apps, schema_editor):
    # Esta función se ejecuta si se revierte la migración
    TipoPedidoCliente = apps.get_model('Gestion_Pedidos_Clientes', 'TipoPedidoCliente')
    EstadoPedidoCliente = apps.get_model('Gestion_Pedidos_Clientes', 'EstadoPedidoCliente')
    
    # No eliminamos los datos en el rollback para evitar problemas con FKs
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('Gestion_Pedidos_Clientes', '0008_pedidocliente_encomendista'),
    ]

    operations = [
        migrations.RunPython(add_catalog_data, remove_catalog_data),
    ]
