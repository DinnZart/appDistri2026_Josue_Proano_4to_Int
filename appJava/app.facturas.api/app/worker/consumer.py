import pika
import json

from app.core.config import RABBITMQ
from app.services.factura_service import FacturaService
from app.models.models import Factura
from app.core.database import Database

db = Database()
factura_service = FacturaService(Factura, db)


def callback(ch, method, properties, body):
    try:
        data = json.loads(body)

        print(f"📥 Evento recibido - pedidoRegistradoEvent: {data}")

        # Mapeo snake_case del evento del productor de pedidos
        pedido_data = {
            "pedido_id": data["pedido_id"],
            "direccion_cliente_id": data["direccion_cliente_id"],
            "cliente_id": data["cliente_id"],
            "nombre_cliente": data["nombre_cliente"],
            "correo_cliente": data["correo_cliente"],
            "fecha_pedido": data["fecha_pedido"],
            "total_pedido": data["total_pedido"]
        }

        factura = factura_service.create_from_pedido(pedido_data)

        print(f"✅ Pedido {data['pedido_id']} persistido y factura generada: {factura.numero_factura}")

    except Exception as e:
        print(f"❌ Error procesando evento: {e}")


def start():
    print("🚀 Iniciando suscriptor RabbitMQ - EcFacturas Worker...")
    print(f"   Cola: {RABBITMQ['queue']}")

    credentials = pika.PlainCredentials(
        RABBITMQ["username"], RABBITMQ["password"]
    )

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=RABBITMQ["hostname"],
            port=RABBITMQ["port"],
            virtual_host=RABBITMQ["virtualHost"],
            credentials=credentials
        )
    )

    channel = connection.channel()
    channel.queue_declare(queue=RABBITMQ["queue"], durable=False)

    channel.basic_consume(
        queue=RABBITMQ["queue"],
        on_message_callback=callback,
        auto_ack=True
    )

    print("📡 Escuchando cola pedidoRegistradoEvent...")
    channel.start_consuming()