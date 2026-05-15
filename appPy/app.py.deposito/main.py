from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse

from models.depositoDto import DepositoDto
from services.depositoService import DepositoService


app = FastAPI()
app.title = "Api service Deposito"
app.version = "0.0.1"

depositoServicio = DepositoService();

@app.get('/', tags=['cuenta'])
def message():
    return HTMLResponse('<h1>Aplicaciones Distribuidas -- Apis en Python</h1>')


@app.post('/deposito', tags=['cuenta'], response_model=dict, status_code=201)
def depositar(deposito: DepositoDto) -> dict:
    depIngresado = depositoServicio.Depositar(deposito)
    return JSONResponse(content=jsonable_encoder(depIngresado))


@app.get('/depositos/', tags=['cuenta'], response_model=dict)
def get_depositos() -> dict:
    depositoLista = depositoServicio.Consultar()
    if not depositoLista:
        return JSONResponse(status_code=404, content={'message':'No existen depositos ingresados'})
    
    return JSONResponse(content=jsonable_encoder(depositoLista))

