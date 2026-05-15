from fastapi import APIRouter, Depends, HTTPException
from app.services.generic_service import GenericService
from app.models.models import Pedido
from app.schemas.schemas import PedidoCreate, PedidoResponse
from app.core.database import Database
from app.services.pedido_service import PedidoService
from app.services.authService import JWTBearerToken

router = APIRouter()

db = Database()
pedido_service = PedidoService(Pedido, db)

@router.get("/pedidos", tags=['pedidos'], response_model=list[PedidoResponse], dependencies=[Depends(JWTBearerToken())])
def get_all():
    return pedido_service.get_all()

@router.get("/pedidos/{id}", tags=['pedidos'], response_model=PedidoResponse)
def get(id: int):
    data = pedido_service.get_by_id(id)
    if not data:
        raise HTTPException(404, "No encontrado")
    return data

@router.post("/pedidos", tags=['pedidos'], response_model=PedidoResponse, dependencies=[Depends(JWTBearerToken())])
def create(pedido: PedidoCreate):
    return pedido_service.create(pedido.dict())

@router.put("/pedidos/{id}", tags=['pedidos'], response_model=PedidoResponse)
def update(id: int, pedido: PedidoCreate):
    data = pedido_service.update(id, pedido.dict())
    if not data:
        raise HTTPException(404, "No encontrado")
    return data


@router.delete("/pedidos/{id}", tags=['pedidos'])
def delete(id: int):
    if not pedido_service.delete(id):
        raise HTTPException(404, "No encontrado")
    return {"message": "Eliminado"}