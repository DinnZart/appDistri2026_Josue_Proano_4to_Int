from jwt import decode, encode


"""
Clase para generar el model
"""
codigoSecreto = "my_secrete_key_app_distri"

def create_token(data: dict) -> str:
    token: str = encode(payload=data, key=codigoSecreto, algorithm="HS256")
    return token


def validate_token(token: str) -> dict:
     data: dict = decode(token, key=codigoSecreto, algorithms=['HS256'])
     return data