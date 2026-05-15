from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PedidoResponse(BaseModel):
    id: int
    direccion_cliente_id: int
    cliente_id: int
    nombre_cliente: str
    correo_cliente: str
    fecha_pedido: datetime
    total_pedido: float

    class Config:
        from_attributes = True


class FacturaCreate(BaseModel):
    pedido_id: int
    numero_factura: str
    fecha_factura: Optional[datetime] = None
    total_factura: float


class FacturaResponse(BaseModel):
    id: int
    pedido_id: int
    numero_factura: str
    fecha_factura: datetime
    total_factura: float

    class Config:
        from_attributes = True


"""clase para validar las credenciales del token"""
class Usuario(BaseModel):
    email: str
    password: str