DATABASE_URL = "mysql+mysqlconnector://root:admin@localhost:3307/EcPedidos"

RABBITMQ = {
    "username": "admin",
    "password": "admin",
    "virtualHost": "/",
    "port": 5672,
    "hostname": "localhost",
    "queue": "clienteDireccionEvent",
    "pedido_queue": "pedidoRegistradoEvent"
}