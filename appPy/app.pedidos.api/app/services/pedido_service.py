from app.services.generic_service import GenericService
from app.core.rabbitmq_producer import RabbitMQProducer
from app.core.config import RABBITMQ
from app.models.models import DireccionCliente


class PedidoService(GenericService):

    def __init__(self, model, database):
        super().__init__(model, database)

    def create(self, data: dict):
        # 1. Guardar en BD
        pedido = super().create(data)

        # 2. Obtener datos del cliente
        session = self.db.get_session()
        try:
            direccion = session.get(DireccionCliente, pedido.direccion_cliente_id)
            cliente_id = direccion.cliente_id if direccion else None
            nombre_cliente = direccion.nombre_completo if direccion else ""
            correo_cliente = direccion.email if direccion else ""
        finally:
            session.close()

        # 3. Publicar evento
        producer = RabbitMQProducer()

        try:
            message = {
                "pedido_id": pedido.id,
                "direccion_cliente_id": pedido.direccion_cliente_id,
                "cliente_id": cliente_id,
                "nombre_cliente": nombre_cliente,
                "correo_cliente": correo_cliente,
                "fecha_pedido": str(pedido.fecha_pedido),
                "total_pedido": float(pedido.total)
            }

            producer.publish(RABBITMQ["pedido_queue"], message)

        finally:
            producer.close()

        return pedido