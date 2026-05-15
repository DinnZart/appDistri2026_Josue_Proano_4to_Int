from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer
from app.services.jwt_manager import validate_token


class JWTBearerToken(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        try:
            data = validate_token(auth.credentials)
        except Exception as e:
            raise HTTPException(status_code=401, detail="Token inválido o expirado")
        
        if data.get('email') != "admin@gmail.com":
            raise HTTPException(status_code=403, detail="Credenciales incorrectas")