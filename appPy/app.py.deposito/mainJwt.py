from fastapi import Depends, FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse

from services.authService import JWTBearerToken
from models.depositoDto import DepositoDto, Usuario
from services.depositoService import DepositoService
"""config para token"""
from services.jwt_manager import create_token



app = FastAPI()
app.title = "Api service Deposito"
app.version = "0.0.1"

depositoServicio = DepositoService();

"""Api para obtener el Token"""
@app.post('/login', tags=['seguridad'])
def login(user: Usuario):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.model_dump())
        return JSONResponse(status_code=200, content=token)


@app.get('/', tags=['cuenta'])
def message():
    return HTMLResponse('<h1>Aplicaciones Distribuidas -- Apis en Python</h1>')


@app.post('/deposito', tags=['cuenta'], response_model=dict, status_code=201, dependencies=[Depends(JWTBearerToken())])
def depositar(deposito: DepositoDto) -> dict:
    depIngresado = depositoServicio.Depositar(deposito)
    return JSONResponse(content=jsonable_encoder(depIngresado))


@app.get('/depositos', tags=['cuenta'], response_model=dict, status_code=200, dependencies=[Depends(JWTBearerToken())])
def get_depositos() -> dict:
    depositoLista = depositoServicio.Consultar()
    if not depositoLista:
        return JSONResponse(status_code=404, content={'message':'No existen datos para la cuenta ingresada'})
    
    return JSONResponse(content=jsonable_encoder(depositoLista))