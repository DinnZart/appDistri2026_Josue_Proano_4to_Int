import json
import pika
from app.core.config import RABBITMQ

class RabbitMQProducer:

    def __init__(self):
        credentials = pika.PlainCredentials(
            RABBITMQ["username"], RABBITMQ["password"]
        )

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=RABBITMQ["hostname"],
                port=RABBITMQ["port"],
                virtual_host=RABBITMQ["virtualHost"],
                credentials=credentials
            )
        )

        self.channel = self.connection.channel()

    def publish(self, queue: str, message: dict):
        self.channel.queue_declare(queue=queue)

        self.channel.basic_publish(
            exchange="",
            routing_key=queue,
            body=json.dumps(message)
        )

        print(f"📤 Mensaje enviado a {queue}: {message}")

    def close(self):
        self.connection.close()