import pika
import json

from app.core.config import RABBITMQ
from app.services.generic_service import GenericService
from app.models.models import DireccionCliente
from app.core.database import Database

db = Database()
service = GenericService(DireccionCliente, db)


def callback(ch, method, properties, body):
    try:
        data = json.loads(body)

        obj = {
            "cliente_id": data["ClienteId"],
            "nombre_completo": data["NombreCompleto"],
            "email": data["Email"],
            "direccion": data["DireccionCompleta"]
        }

        service.create(obj)

        print("✅ Insertado:", obj)

    except Exception as e:
        print("❌ Error:", e)


def start():
    print("🚀 Iniciando suscriptor RabbitMQ...")
    print(RABBITMQ["username"])
    print(RABBITMQ["password"])
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
    print("***ok***")
    channel.queue_declare(queue=RABBITMQ["queue"], durable=True)
    

    channel.basic_consume(
        queue=RABBITMQ["queue"],
        on_message_callback=callback,
        auto_ack=True
    )

    print("📡 Escuchando RabbitMQ...")
    channel.start_consuming()