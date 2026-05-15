# 🧾 EcFacturas - API + Worker con Arquitectura Distribuida

Sistema desarrollado en **Python** que implementa un **CRUD de Facturas** con arquitectura en capas, integración con **PostgreSQL** y comunicación asíncrona mediante **RabbitMQ**.

---

## 📌 Descripción

**EcFacturas** es un microservicio consumidor diseñado para:

- Escuchar el evento `pedidoRegistradoEvent` desde **RabbitMQ**
- Persistir los datos del pedido en **PostgreSQL**
- Generar automáticamente una **factura** asociada al pedido
- Exponer endpoints **CRUD** para gestión de facturas

### Tecnologías:
- Python 3.13
- FastAPI
- SQLAlchemy (Code First)
- PostgreSQL (puerto 5434)
- RabbitMQ
- JWT (Bearer Token)

---

## 🏗️ Arquitectura

### 🔹 API (Productor de datos / CRUD)
- Expone endpoints CRUD para `Factura`
- Consulta de `Pedido` persistidos
- Autenticación con JWT Bearer Token
- Guarda datos en PostgreSQL (`EcFacturas`)

### 🔹 Worker (Consumidor de eventos)
- Escucha la cola `pedidoRegistradoEvent`
- Persiste el pedido en la tabla `pedido`
- Genera automáticamente una factura en la tabla `factura`

---

## 📁 Estructura del Proyecto

```
app.facturas.api/
├── app/
│   ├── core/
│   │   ├── config.py              # Conexión PostgreSQL + RabbitMQ
│   │   ├── database.py            # Engine SQLAlchemy
│   │   └── rabbitmq_producer.py   # Productor RabbitMQ (futuro uso)
│   ├── models/
│   │   └── models.py              # Entidades Pedido + Factura (Code First)
│   ├── schemas/
│   │   └── schemas.py             # DTOs Pydantic
│   ├── services/
│   │   ├── generic_service.py     # CRUD genérico reutilizable
│   │   ├── factura_service.py     # Lógica de negocio facturas
│   │   ├── jwt_manager.py         # Generación/validación JWT
│   │   └── authService.py         # Bearer Token middleware
│   ├── api/
│   │   └── routes.py              # Endpoints REST
│   └── worker/
│       └── consumer.py            # Consumidor pedidoRegistradoEvent
├── main_api.py                    # Entry point API FastAPI
├── main_worker.py                 # Entry point Worker RabbitMQ
└── requirements.txt               # Dependencias
```

---

## 🗄️ Modelo de Datos (PostgreSQL - EcFacturas)

### Tabla `pedido`
| Campo | Tipo | Descripción |
|---|---|---|
| `id` | Integer (PK) | ID del pedido (recibido del evento) |
| `direccion_cliente_id` | Integer | FK dirección del cliente |
| `cliente_id` | Integer | ID del cliente |
| `nombre_cliente` | String(255) | Nombre completo |
| `correo_cliente` | String(255) | Email del cliente |
| `fecha_pedido` | DateTime | Fecha del pedido |
| `total_pedido` | Numeric(10,2) | Total del pedido |

### Tabla `factura`
| Campo | Tipo | Descripción |
|---|---|---|
| `id` | Integer (PK, auto) | ID autoincremental |
| `pedido_id` | Integer (FK) | Referencia a `pedido.id` |
| `numero_factura` | String(50, unique) | Formato: `FAC-YYYYMMDD-{pedido_id}` |
| `fecha_factura` | DateTime | Fecha de generación |
| `total_factura` | Numeric(10,2) | Total de la factura |

---

## 🚀 Ejecución

1. Base de datos PostgreSQL (ya creada):
   - Host: `localhost:5434`
   - User: `postgres`
   - Password: `admin`
   - Database: `EcFacturas`

2. Crear ambiente virtual:
   ```
   py -3.13 -m venv myenv
   myenv\Scripts\activate
   ```

3. Instalar dependencias:
   ```
   pip install -r requirements.txt
   ```

4. Ejecutar API (Code-First crea las tablas automáticamente):
   ```
   uvicorn main_api:app --reload --port 8001
   ```

5. Ejecutar Worker:
   ```
   python main_worker.py
   ```

6. Levantar RabbitMQ (si no está corriendo):
   ```
   docker run -d -p 5672:5672 -p 15672:15672 rabbitmq:3-management
   ```

---

## 📡 Endpoints API

### Seguridad
| Método | Endpoint | Descripción |
|---|---|---|
| POST | `/login` | Obtener token JWT |

**Credenciales:** `admin@gmail.com` / `admin`

### Facturas (CRUD)
| Método | Endpoint | Auth | Descripción |
|---|---|---|---|
| GET | `/facturas` | 🔒 JWT | Listar todas las facturas |
| GET | `/facturas/{id}` | ❌ | Obtener factura por ID |
| POST | `/facturas` | 🔒 JWT | Crear factura manualmente |
| PUT | `/facturas/{id}` | ❌ | Actualizar factura |
| DELETE | `/facturas/{id}` | ❌ | Eliminar factura |

### Pedidos (Consulta)
| Método | Endpoint | Auth | Descripción |
|---|---|---|---|
| GET | `/pedidos` | 🔒 JWT | Listar pedidos persistidos |
| GET | `/pedidos/{id}` | ❌ | Obtener pedido por ID |

---

## 📡 Ejemplo de Evento

Entrada (Worker - cola `pedidoRegistradoEvent`):
```json
{
   "pedido_id": 15, 
   "direccion_cliente_id": 3, 
   "cliente_id": 2, 
   "nombre_cliente": "Josue Proaño", 
   "correo_cliente": "josue@proano.com", 
   "fecha_pedido": "2026-05-09 06:28:58", 
   "total_pedido": 32.25
}
```

Resultado automático en tabla `factura`:
```json
{
   "id": 1,
   "pedido_id": 15,
   "numero_factura": "FAC-20260509-15",
   "fecha_factura": "2026-05-09T14:20:00",
   "total_factura": 32.25
}
```

---

## 📌 Autor

Proyecto para aprendizaje de Aplicaciones Distribuidas.
