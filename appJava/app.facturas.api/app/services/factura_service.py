from datetime import datetime
from sqlalchemy.orm import Session

from app.services.generic_service import GenericService
from app.models.models import Pedido, Factura


class FacturaService(GenericService):

    def __init__(self, model, database):
        super().__init__(model, database)

    def create_from_pedido(self, pedido_data: dict):
        """
        Persiste el pedido recibido del evento y genera automáticamente una factura.
        1. Inserta el pedido en la tabla 'pedido'
        2. Genera numero_factura con formato FAC-{YYYYMMDD}-{pedido_id}
        3. Crea la factura asociada
        """
        session: Session = self.db.get_session()
        try:
            # 1. Persistir pedido
            pedido = Pedido(
                id=pedido_data["pedido_id"],
                direccion_cliente_id=pedido_data["direccion_cliente_id"],
                cliente_id=pedido_data["cliente_id"],
                nombre_cliente=pedido_data["nombre_cliente"],
                correo_cliente=pedido_data["correo_cliente"],
                fecha_pedido=pedido_data["fecha_pedido"],
                total_pedido=pedido_data["total_pedido"]
            )
            session.add(pedido)
            session.flush()

            # 2. Generar número de factura
            fecha_str = datetime.now().strftime("%Y%m%d")
            numero_factura = f"FAC-{fecha_str}-{pedido.id}"

            # 3. Crear factura
            factura = Factura(
                pedido_id=pedido.id,
                numero_factura=numero_factura,
                fecha_factura=datetime.now(),
                total_factura=pedido_data["total_pedido"]
            )
            session.add(factura)
            session.commit()
            session.refresh(factura)

            print(f"✅ Factura generada: {numero_factura} para pedido {pedido.id}")
            return factura

        except Exception as e:
            session.rollback()
            print(f"❌ Error al crear factura desde pedido: {e}")
            raise e
        finally:
            session.close()
