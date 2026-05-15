from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey
from app.core.database import Base


class DireccionCliente(Base):
    __tablename__ = "direcciones_clientes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cliente_id = Column(Integer)
    nombre_completo = Column(String(255))
    email = Column(String(255))
    direccion = Column(String(500))


class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    direccion_cliente_id = Column(Integer, ForeignKey("direcciones_clientes.id"))
    fecha_pedido = Column(DateTime)
    total = Column(Numeric(10, 2))


