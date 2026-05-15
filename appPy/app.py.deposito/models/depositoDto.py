from typing import Optional
from pydantic import BaseModel, Field

"""clase para obtener y registrar un deposito por el API"""
class DepositoDto(BaseModel):
        id: Optional[int] = None
        nombre:str = Field(min_length=5, max_length=30)
        tipo:str = Field(min_length=5, max_length=15)
        cuenta:str = Field(min_length=5, max_length=10)
        valor:float = Field(ge=1, le=1000000)


"""clase para validar las credenciales del token"""
class Usuario(BaseModel):
    email:str
    password:str