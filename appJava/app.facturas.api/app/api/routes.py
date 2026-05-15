from fastapi import APIRouter, Depends, HTTPException
from app.services.generic_service import GenericService
from app.services.factura_service import FacturaService
from app.models.models import Factura, Pedido
from app.schemas.schemas import FacturaCreate, FacturaResponse, PedidoResponse
from app.core.database import Database
from app.services.authService import JWTBearerToken
from datetime import datetime

router = APIRouter()

db = Database()
factura_service = FacturaService(Factura, db)
pedido_service = GenericService(Pedido, db)


# ==================== ENDPOINTS FACTURAS ====================

@router.get("/facturas", tags=['facturas'], response_model=list[FacturaResponse], dependencies=[Depends(JWTBearerToken())])
def get_all_facturas():
    return factura_service.get_all()


@router.get("/facturas/{id}", tags=['facturas'], response_model=FacturaResponse)
def get_factura(id: int):
    data = factura_service.get_by_id(id)
    if not data:
        raise HTTPException(404, "Factura no encontrada")
    return data


@router.post("/facturas", tags=['facturas'], response_model=FacturaResponse, dependencies=[Depends(JWTBearerToken())])
def create_factura(factura: FacturaCreate):
    factura_data = factura.dict()
    if factura_data.get("fecha_factura") is None:
        factura_data["fecha_factura"] = datetime.now()
    return factura_service.create(factura_data)


@router.put("/facturas/{id}", tags=['facturas'], response_model=FacturaResponse)
def update_factura(id: int, factura: FacturaCreate):
    data = factura_service.update(id, factura.dict())
    if not data:
        raise HTTPException(404, "Factura no encontrada")
    return data


@router.delete("/facturas/{id}", tags=['facturas'])
def delete_factura(id: int):
    if not factura_service.delete(id):
        raise HTTPException(404, "Factura no encontrada")
    return {"message": "Factura eliminada correctamente"}


# ==================== ENDPOINTS PEDIDOS (consulta) ====================

@router.get("/pedidos", tags=['pedidos'], response_model=list[PedidoResponse], dependencies=[Depends(JWTBearerToken())])
def get_all_pedidos():
    return pedido_service.get_all()


@router.get("/pedidos/{id}", tags=['pedidos'], response_model=PedidoResponse)
def get_pedido(id: int):
    data = pedido_service.get_by_id(id)
    if not data:
        raise HTTPException(404, "Pedido no encontrado")
    return data