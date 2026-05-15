from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Pedido(Base):
    __tablename__ = "pedido"

    id = Column(Integer, primary_key=True, index=True, autoincrement=False)
    direccion_cliente_id = Column(Integer, nullable=False)
    cliente_id = Column(Integer, nullable=False)
    nombre_cliente = Column(String(255), nullable=False)
    correo_cliente = Column(String(255), nullable=False)
    fecha_pedido = Column(DateTime, nullable=False)
    total_pedido = Column(Numeric(10, 2), nullable=False)

    facturas = relationship("Factura", back_populates="pedido")


class Factura(Base):
    __tablename__ = "factura"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    pedido_id = Column(Integer, ForeignKey("pedido.id"), nullable=False)
    numero_factura = Column(String(50), unique=True, nullable=False)
    fecha_factura = Column(DateTime, nullable=False)
    total_factura = Column(Numeric(10, 2), nullable=False)

    pedido = relationship("Pedido", back_populates="facturas")
