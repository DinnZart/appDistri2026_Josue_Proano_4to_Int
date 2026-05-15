DATABASE_URL = "postgresql+psycopg2://postgres:admin@localhost:5434/EcFacturas"

RABBITMQ = {
    "username": "admin",
    "password": "admin",
    "virtualHost": "/",
    "port": 5672,
    "hostname": "localhost",
    "queue": "pedidoRegistradoEvent",
}