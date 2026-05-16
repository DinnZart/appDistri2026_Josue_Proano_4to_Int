# 📦 EcPedidos — Documentación de Despliegue de Módulo

> **Proyecto:** EcPedidos — Gestión de Pedidos con Arquitectura Distribuida  
> **Materia:** Aplicaciones Distribuidas  
> **Institución:** Instituto Superior Universitario Japón  
> **Docente:** Ing. Geovanny Cholca  
> **Estudiante:** Josue Ismael Proaño Arroyo  
> **Nivel/Paralelo:** 4to — Desarrollo de Software  
> **Fecha:** 15/05/2026  

---

## Tabla de Contenidos

1. [Introducción](#1-introducción)
2. [Descripción de la Arquitectura](#2-descripción-de-la-arquitectura)
3. [Configuración del Entorno](#3-configuración-del-entorno)
4. [Evidencias de Despliegue](#4-evidencias-de-despliegue)
5. [Referencia del CRUD](#5-referencia-del-crud)
6. [Integración con RabbitMQ](#6-integración-con-rabbitmq)
7. [Seguridad — Autenticación JWT](#7-seguridad--autenticación-jwt)
8. [Conclusiones](#8-conclusiones)
9. [Referencias](#9-referencias)

---

## 1. Introducción

El presente documento describe el proceso de análisis, configuración y despliegue del módulo **EcPedidos**, una API REST desarrollada en **Python con FastAPI** orientada a la gestión de pedidos dentro de un ecosistema de microservicios. El módulo forma parte del proyecto académico de **Aplicaciones Distribuidas** y demuestra buenas prácticas en:

- Arquitectura en capas (Core / Models / Schemas / Services / API)
- Persistencia con **SQLAlchemy** en modo *Code First* sobre **MySQL**
- Comunicación asíncrona entre microservicios mediante **RabbitMQ**
- Seguridad de endpoints mediante tokens **JWT**
- Separación de responsabilidades entre el proceso **API (Productor)** y el proceso **Worker (Consumidor)**

El módulo EcPedidos actúa como el núcleo transaccional del sistema distribuido: recibe los pedidos de los clientes, los persiste en la base de datos y notifica al resto de los servicios mediante eventos publicados en la cola de mensajería.

> **📝 Completar:** Amplíe aquí con el contexto específico del entorno académico, los objetivos del módulo dentro del sistema distribuido mayor y cualquier decisión de diseño relevante tomada durante el desarrollo.

---

## 2. Descripción de la Arquitectura

La arquitectura del módulo EcPedidos sigue el patrón de **microservicios**, con una separación clara entre el proceso que expone la API REST y el proceso Worker que consume mensajes de la cola. Todos los componentes se ejecutan de forma independiente y se comunican a través de RabbitMQ.

### 2.1 Stack tecnológico

| Capa | Tecnología |
|---|---|
| Backend / API REST | Python 3 · FastAPI · Uvicorn |
| ORM / Persistencia | SQLAlchemy (Code First) |
| Base de datos | MySQL (puerto `3307`) |
| Mensajería asíncrona | RabbitMQ 3 · Pika |
| Seguridad | PyJWT — Bearer Token |
| Validación de datos | Pydantic v2 |
| Documentación de API | Swagger UI (integrado en FastAPI) |
| Orquestación (RabbitMQ) | Docker (contenedor `rabbitmq:3-management`) |

### 2.2 Diagrama de arquitectura

```
┌──────────────┐    POST /pedidos     ┌───────────────────────────┐
│   Cliente    │  ────────────────▶   │   main_api.py             │
│   HTTP       │  (JWT en header)     │   FastAPI · Uvicorn        │
└──────────────┘                      │   Puerto: 8000             │
                                      └────────────┬──────────────┘
                                                   │
                        ┌──────────────────────────┼──────────────────────────┐
                        │                          │                          │
                        ▼                          ▼                          ▼
              ┌─────────────────┐      ┌──────────────────┐      ┌──────────────────┐
              │  pedido_service │      │   MySQL DB        │      │  RabbitMQ        │
              │  (capa Service) │ ───▶ │  EcPedidos        │      │  Broker          │
              └─────────────────┘      │  tablas:          │      │  Puerto: 5672    │
                                       │  · pedidos        │      │  UI:  15672      │
                                       │  · dir_clientes   │      └──────────┬───────┘
                                       └──────────────────┘                 │
                                                                             │ pedidoRegistradoEvent
                                                                             ▼
                                                                  ┌──────────────────┐
                                                                  │  main_worker.py  │
                                                                  │  (Consumidor)    │
                                                                  │  clienteDirEvent │
                                                                  └──────────────────┘
```

> **📝 Completar:** Reemplace o complemente el diagrama con el diagrama real del proyecto e incluya una descripción del flujo completo de datos entre todos los módulos del sistema distribuido.

### 2.3 Estructura del proyecto

```
app.pedidos.api/
├── app/
│   ├── api/
│   │   └── routes.py          # Endpoints CRUD de Pedidos
│   ├── core/
│   │   ├── config.py          # Configuración DB y RabbitMQ
│   │   ├── database.py        # Engine SQLAlchemy y sesión
│   │   └── rabbitmq_producer.py  # Productor de mensajes Pika
│   ├── models/
│   │   └── models.py          # Modelos ORM: Pedido, DireccionCliente
│   ├── schemas/
│   │   └── schemas.py         # Schemas Pydantic: Request / Response
│   ├── services/
│   │   ├── authService.py     # Dependencia JWT Bearer
│   │   ├── generic_service.py # CRUD genérico reutilizable
│   │   ├── jwt_manager.py     # Utilidades de JWT
│   │   └── pedido_service.py  # Lógica de negocio de Pedidos
│   └── worker/                # Consumidor RabbitMQ (Worker)
├── main_api.py                # Punto de entrada de la API
├── main_worker.py             # Punto de entrada del Worker
└── requirements.txt           # Dependencias Python
```

---

## 3. Configuración del Entorno

### 3.1 Requisitos previos

- [ ] Python 3.10 o superior instalado
- [ ] MySQL corriendo en `localhost:3307` (o el puerto configurado)
- [ ] Docker Desktop instalado (para levantar RabbitMQ)
- [ ] Base de datos `EcPedidos` creada en MySQL

### 3.2 Variables de configuración (`app/core/config.py`)

Toda la configuración del módulo se centraliza en el archivo `config.py`. No utiliza variables de entorno externas; los valores se definen directamente en el código:

| Variable | Descripción | Valor por defecto |
|---|---|---|
| `DATABASE_URL` | Cadena de conexión SQLAlchemy | `mysql+mysqlconnector://root:admin@localhost:3307/EcPedidos` |
| `RABBITMQ["hostname"]` | Host del broker RabbitMQ | `localhost` |
| `RABBITMQ["port"]` | Puerto AMQP de RabbitMQ | `5672` |
| `RABBITMQ["username"]` | Usuario de RabbitMQ | `admin` |
| `RABBITMQ["password"]` | Contraseña de RabbitMQ | `admin` |
| `RABBITMQ["virtualHost"]` | Virtual host de RabbitMQ | `/` |
| `RABBITMQ["queue"]` | Cola escuchada por el Worker | `clienteDireccionEvent` |
| `RABBITMQ["pedido_queue"]` | Cola publicada por la API | `pedidoRegistradoEvent` |

> **📝 Completar:** En un entorno de producción, migre estos valores a variables de entorno (`.env`) usando la librería `python-dotenv`.

### 3.3 Dependencias Python (`requirements.txt`)

```text
fastapi
uvicorn
sqlalchemy
mysql-connector-python
pydantic
pika
PyJWT
```

### 3.4 Proceso de levantamiento

**Paso 0 — Crear la base de datos en MySQL:**

```sql
CREATE DATABASE IF NOT EXISTS EcPedidos;
```

**Paso 1 — Instalar dependencias:**

```bash
pip install -r requirements.txt
```

**Paso 2 — Levantar RabbitMQ con Docker:**

```bash
docker run -d -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

**Paso 3 — Iniciar la API (Productor):**

```bash
uvicorn main_api:app --reload
```

> La API crea las tablas automáticamente en MySQL mediante `Base.metadata.create_all()` al arrancar (*Code First*).

**Paso 4 — Iniciar el Worker (Consumidor) en una terminal separada:**

```bash
python main_worker.py
```

**Paso 5 — Acceder a la documentación interactiva:**

```
Swagger UI  →  http://localhost:8000/docs
RabbitMQ UI →  http://localhost:15672  (usuario: admin / contraseña: admin)
```

---

## 4. Evidencias de Despliegue

A continuación se presentan las capturas de pantalla que evidencian el correcto funcionamiento del entorno desplegado.

### 4.1 Docker Desktop — Contenedor RabbitMQ activo

> **📷 Insertar:** Captura de Docker Desktop mostrando el contenedor `rabbitmq:3-management` en estado `Running`.

---

### 4.2 Base de datos creada en MySQL

> **📷 Insertar:** Captura del cliente MySQL (MySQL Workbench u otro) mostrando la base de datos `EcPedidos` con las tablas `pedidos` y `direcciones_clientes` generadas automáticamente por SQLAlchemy.

Tablas esperadas tras el arranque de la API:

```
EcPedidos
├── pedidos
│   ├── id              INT (PK, autoincrement)
│   ├── direccion_cliente_id  INT (FK → direcciones_clientes.id)
│   ├── fecha_pedido    DATETIME
│   └── total           DECIMAL(10,2)
└── direcciones_clientes
    ├── id              INT (PK, autoincrement)
    ├── cliente_id      INT
    ├── nombre_completo VARCHAR(255)
    ├── email           VARCHAR(255)
    └── direccion       VARCHAR(500)
```

---

### 4.3 API corriendo — Mensaje de bienvenida

> **📷 Insertar:** Captura del navegador en `http://localhost:8000/` mostrando la respuesta JSON `{"message": "API EcPedidos funcionando"}`.

---

### 4.4 Swagger UI con endpoints disponibles

> **📷 Insertar:** Captura de `http://localhost:8000/docs` mostrando los grupos de endpoints `pedidos` y `seguridad` expandidos.

---

### 4.5 Prueba con Postman o Swagger — Obtención del Token JWT

> **📷 Insertar:** Captura de la petición `POST /login` con el body `{"email": "admin@gmail.com", "password": "admin"}` y la respuesta con el token JWT generado.

---

### 4.6 Prueba con Postman o Swagger — CRUD de Pedidos

> **📷 Insertar:** Capturas de las siguientes peticiones exitosas usando el token JWT en el header `Authorization: Bearer <token>`:
> - `POST /pedidos` — Crear un pedido
> - `GET /pedidos` — Listar todos los pedidos
> - `GET /pedidos/{id}` — Obtener pedido por ID
> - `PUT /pedidos/{id}` — Actualizar un pedido
> - `DELETE /pedidos/{id}` — Eliminar un pedido

---

### 4.7 RabbitMQ Management UI — Cola con mensaje publicado

> **📷 Insertar:** Captura de `http://localhost:15672` mostrando la cola `pedidoRegistradoEvent` con al menos un mensaje encolado tras haber creado un pedido.

---

## 5. Referencia del CRUD

Las operaciones CRUD gestionan los recursos del módulo a través de los endpoints RESTful expuestos por la API.  
Los endpoints marcados con 🔒 requieren autenticación mediante **Bearer Token JWT**.

### 5.1 Entidad: `Pedido`

| Método HTTP | Endpoint | Auth | Descripción |
|---|---|---|---|
| `GET` | `/pedidos` | 🔒 JWT | Obtiene la lista de todos los pedidos registrados |
| `GET` | `/pedidos/{id}` | Abierto | Obtiene los datos de un pedido por su ID |
| `POST` | `/pedidos` | 🔒 JWT | Crea un nuevo pedido y publica evento en RabbitMQ |
| `PUT` | `/pedidos/{id}` | Abierto | Actualiza los datos de un pedido existente |
| `DELETE` | `/pedidos/{id}` | Abierto | Elimina un pedido por su ID |

#### Schema de entrada — `PedidoCreate`

```json
{
  "direccion_cliente_id": 1,
  "fecha_pedido": "2026-05-15T19:00:00",
  "total": 150.75
}
```

#### Schema de respuesta — `PedidoResponse`

```json
{
  "id": 1,
  "direccion_cliente_id": 1,
  "fecha_pedido": "2026-05-15T19:00:00",
  "total": 150.75
}
```

---

### 5.2 Entidad: `DireccionCliente` _(tabla de apoyo, gestionada por el Worker)_

Esta entidad es poblada automáticamente por el **Worker** al consumir eventos de la cola `clienteDireccionEvent` publicados por el módulo **EcClientes**. La API de EcPedidos la consume en modo lectura al crear un pedido para enriquecer el evento publicado.

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | `INT` (PK) | Identificador único |
| `cliente_id` | `INT` | ID del cliente en el sistema EcClientes |
| `nombre_completo` | `VARCHAR(255)` | Nombre completo del cliente |
| `email` | `VARCHAR(255)` | Correo electrónico del cliente |
| `direccion` | `VARCHAR(500)` | Dirección de entrega del cliente |

---

### 5.3 Endpoint de Autenticación

| Método HTTP | Endpoint | Descripción |
|---|---|---|
| `POST` | `/login` | Genera un token JWT con las credenciales del administrador |

#### Body de login

```json
{
  "email": "admin@gmail.com",
  "password": "admin"
}
```

#### Respuesta — Token JWT (string)

```
"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

---

## 6. Integración con RabbitMQ

El módulo EcPedidos implementa un patrón **Productor / Consumidor** para la comunicación asíncrona entre microservicios.

### 6.1 Flujo del Productor (API)

Al ejecutar `POST /pedidos`, el servicio `PedidoService` realiza el siguiente flujo:

```
1. Guardar el pedido en MySQL (tabla `pedidos`)
2. Consultar la tabla `direcciones_clientes` para obtener datos del cliente
3. Construir el mensaje de evento `pedidoRegistradoEvent`
4. Publicar el mensaje en RabbitMQ mediante RabbitMQProducer
5. Retornar el objeto Pedido creado al cliente HTTP
```

#### Estructura del mensaje publicado — `pedidoRegistradoEvent`

```json
{
  "pedido_id": 1,
  "direccion_cliente_id": 10,
  "cliente_id": 5,
  "nombre_cliente": "Juan Pérez",
  "correo_cliente": "juan@mail.com",
  "fecha_pedido": "2026-05-15 19:00:00",
  "total_pedido": 150.75
}
```

### 6.2 Flujo del Consumidor (Worker)

El proceso `main_worker.py` escucha la cola `clienteDireccionEvent` (publicada por **EcClientes**) e inserta los datos de dirección del cliente en la tabla `direcciones_clientes` de la base de datos local.

#### Estructura del mensaje consumido — `clienteDireccionEvent`

```json
{
  "ClienteId": 10,
  "NombreCompleto": "Juan Pérez",
  "Email": "juan@mail.com",
  "Direccion": "Quito, Ecuador"
}
```

### 6.3 Configuración del productor RabbitMQ

El productor se instancia automáticamente en `PedidoService.create()` con la configuración centralizada en `config.py`:

```python
# app/core/rabbitmq_producer.py
producer = RabbitMQProducer()          # Abre conexión con parámetros de config.py
producer.publish("pedidoRegistradoEvent", message)   # Publica en la cola
producer.close()                       # Cierra la conexión
```

---

## 7. Seguridad — Autenticación JWT

Los endpoints críticos (`GET /pedidos` y `POST /pedidos`) están protegidos mediante el esquema **HTTP Bearer Token** implementado con `PyJWT`.

### 7.1 Flujo de autenticación

```
Cliente ──▶ POST /login ──▶ Valida credenciales hardcoded
                         ──▶ Retorna token JWT firmado

Cliente ──▶ GET /pedidos  (Authorization: Bearer <token>)
         ──▶ JWTBearerToken.validate_token()
         ──▶ Verifica email == "admin@gmail.com"
         ──▶ Acceso concedido / HTTP 401 o 403
```

### 7.2 Dependencia FastAPI — `JWTBearerToken`

La clase `JWTBearerToken(HTTPBearer)` en `authService.py` se inyecta como dependencia en los routers protegidos:

```python
@router.get("/pedidos", dependencies=[Depends(JWTBearerToken())])
@router.post("/pedidos", dependencies=[Depends(JWTBearerToken())])
```

| Código HTTP | Situación |
|---|---|
| `200` | Token válido y email correcto |
| `401` | Token inválido, expirado o ausente |
| `403` | Token válido pero credenciales incorrectas |

> **📝 Completar:** Para producción, migre las credenciales a variables de entorno y use una clave secreta (`SECRET_KEY`) externa para firmar los tokens.

---

## 8. Conclusiones

> **📝 Completar:** Reemplace cada punto con sus reflexiones reales al concluir el módulo.

- **[C1]** _(FastAPI y arquitectura en capas)_ — Describa lo aprendido sobre la organización del código en capas (api / services / models / schemas / core) y cómo favorece el mantenimiento y la escalabilidad.
- **[C2]** _(SQLAlchemy Code First)_ — Reflexione sobre las ventajas del enfoque *Code First* en el que los modelos Python generan automáticamente el esquema de base de datos en MySQL.
- **[C3]** _(Comunicación asíncrona con RabbitMQ)_ — Evalúe el patrón Productor/Consumidor implementado y cómo desacopla los microservicios entre sí (EcClientes → EcPedidos).
- **[C4]** _(Seguridad con JWT)_ — Describa el funcionamiento del esquema de autenticación implementado y las mejoras que aplicaría en un entorno de producción real.
- **[C5]** _(Desafíos y soluciones)_ — Detalle los obstáculos encontrados durante el desarrollo y despliegue (por ejemplo, manejo de tokens malformados, configuración de puertos) y cómo fueron resueltos.
- **[C6]** _(Valor académico-profesional)_ — Exponga el valor de esta práctica para su formación como desarrollador de software en el ámbito de los sistemas distribuidos.

---

## 9. Referencias

- Ramírez, S. (2024). *FastAPI Documentation*. https://fastapi.tiangolo.com
- SQLAlchemy Authors. (2024). *SQLAlchemy Documentation*. https://docs.sqlalchemy.org
- RabbitMQ Team. (2024). *RabbitMQ Documentation*. https://www.rabbitmq.com/docs
- Pika Authors. (2024). *Pika — Python AMQP Client Library*. https://pika.readthedocs.io
- Docker Inc. (2024). *Docker Documentation*. https://docs.docker.com
- > **📝 Completar:** Agregue las referencias bibliográficas adicionales utilizadas en formato APA o IEEE.

---

<sub>Instituto Superior Universitario Japón · Aplicaciones Distribuidas · 2026</sub>
