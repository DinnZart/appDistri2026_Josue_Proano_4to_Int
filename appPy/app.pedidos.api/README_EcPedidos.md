# 🚀 EcPedidos - API + Worker con Arquitectura Distribuida

Sistema desarrollado en **Python** que implementa un **CRUD de Pedidos** con arquitectura en capas, integración con **MySQL** y comunicación asíncrona mediante **RabbitMQ**.

---

## 📌 Descripción

**EcPedidos** es un proyecto diseñado para demostrar buenas prácticas en:

- Desarrollo de APIs con **FastAPI**
- Persistencia con **SQLAlchemy (Code First)**
- Arquitectura en capas
- Uso de **RabbitMQ** para comunicación asíncrona
- Separación entre API (productor) y Worker (consumidor)

---

## 🏗️ Arquitectura

### 🔹 API (Productor)
- Expone endpoints CRUD para `Pedido`
- Guarda datos en MySQL
- Publica eventos en RabbitMQ (`pedidoRegistradoEvent`)

### 🔹 Worker (Consumidor)
- Escucha la cola `clienteDireccionEvent`
- Inserta datos en la tabla `DireccionesClientes`

---

## 📁 Estructura del Proyecto

proyecto_pedidos/
├── app/
│   ├── core/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── api/
│   └── worker/
├── main_api.py
├── main_worker.py
└── requirements.txt

---

## 🚀 Ejecución

1. Crear base de datos:
   CREATE DATABASE EcPedidos;

2. Instalar dependencias:
   pip install -r requirements.txt

3. Ejecutar API:
   uvicorn main_api:app --reload

4. Ejecutar Worker:
   python main_worker.py

5. Levantar RabbitMQ:
   docker run -d -p 5672:5672 -p 15672:15672 rabbitmq:3-management

---

## 📡 Ejemplo de Evento

Entrada (Worker):
{
  "ClienteId": 10,
  "NombreCompleto": "Juan Perez",
  "Email": "juan@mail.com",
  "Direccion": "Quito"
}

Salida (API):
{
  "id": 1,
  "direccion_cliente_id": 10,
  "fecha_pedido": "2026-03-27T19:00:00",
  "total": 150.75
}

---

## 🎯 Tecnologías

- Python 3
- FastAPI
- SQLAlchemy
- MySQL
- RabbitMQ

---

## 📌 Autor

Proyecto para aprendizaje de Aplicaciones Distribuidas.
