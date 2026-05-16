# 🧾 EcFacturas — Documentación de Despliegue de Módulo

> **Proyecto:** EcFacturas — Generación y Gestión de Facturas (Microservicio Consumer)  
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
3. [Configuración con Docker](#3-configuración-con-docker)
4. [Evidencias de Despliegue](#4-evidencias-de-despliegue)
5. [Referencia del CRUD](#5-referencia-del-crud)
6. [Flujo del Worker RabbitMQ](#6-flujo-del-worker-rabbitmq)
7. [Conclusiones](#7-conclusiones)
8. [Referencias](#8-referencias)

---

## 1. Introducción

El presente documento describe el proceso de análisis, configuración y despliegue del módulo **EcFacturas**, un microservicio desarrollado en **Python** con el framework **FastAPI** que actúa como **consumidor de eventos** dentro del sistema distribuido de la plataforma de comercio electrónico.

Este módulo desempeña un rol crítico en la cadena de procesamiento de pedidos: al recibir el evento `pedidoRegistradoEvent` publicado en la cola de **RabbitMQ** por el módulo `EcPedidos`, el Worker de EcFacturas persiste el pedido en su propia base de datos **PostgreSQL** y genera automáticamente una factura asociada. Adicionalmente, expone endpoints RESTful que permiten consultar y gestionar las facturas generadas.

Dentro del ecosistema de microservicios del sistema distribuido, EcFacturas representa la capa de **facturación y trazabilidad financiera**, conectando la gestión de pedidos con el registro contable de cada transacción mediante comunicación asíncrona orientada a eventos.

> **📝 Completar:** Amplíe aquí con los objetivos académicos específicos del módulo y su relevancia dentro del sistema distribuido.

---

## 2. Descripción de la Arquitectura

La arquitectura del módulo EcFacturas combina el patrón de **microservicios** con **comunicación asíncrona orientada a eventos** (Event-Driven Architecture). El módulo opera en dos modos de ejecución independientes:

- **API REST** (`main_api.py`): Procesa solicitudes HTTP síncronas para la gestión CRUD de facturas.
- **Worker** (`main_worker.py`): Escucha de forma continua la cola `pedidoRegistradoEvent` en RabbitMQ y genera facturas automáticamente al recibir un evento.

### 2.1 Stack tecnológico

| Capa | Tecnología |
|---|---|
| Lenguaje | Python 3.13 |
| Framework API | FastAPI + Uvicorn |
| ORM / Code-First | SQLAlchemy |
| Base de datos | PostgreSQL (puerto `5434`) |
| Mensajería asíncrona | RabbitMQ (Pika) + cola `pedidoRegistradoEvent` |
| Validación de esquemas | Pydantic |
| Autenticación | JWT Bearer Token (PyJWT) |
| Documentación de API | Swagger UI (integrado en FastAPI) |
| Orquestación | Docker / Docker Compose |

### 2.2 Estructura del proyecto

```
app.facturas.api/
├── app/
│   ├── core/
│   │   ├── config.py              # Cadena de conexión PostgreSQL + config RabbitMQ
│   │   ├── database.py            # Engine y sesión SQLAlchemy
│   │   └── rabbitmq_producer.py   # Productor RabbitMQ (uso futuro)
│   ├── models/
│   │   └── models.py              # Entidades Pedido + Factura (Code First)
│   ├── schemas/
│   │   └── schemas.py             # DTOs Pydantic (request/response)
│   ├── services/
│   │   ├── generic_service.py     # CRUD genérico reutilizable
│   │   ├── factura_service.py     # Lógica de negocio de facturas
│   │   ├── jwt_manager.py         # Generación y validación de JWT
│   │   └── authService.py         # Middleware Bearer Token (JWTBearerToken)
│   ├── api/
│   │   └── routes.py              # Definición de endpoints REST
│   └── worker/
│       └── consumer.py            # Consumidor del evento pedidoRegistradoEvent
├── main_api.py                    # Entry point — API FastAPI
├── main_worker.py                 # Entry point — Worker RabbitMQ
└── requirements.txt               # Dependencias Python
```

### 2.3 Diagrama de arquitectura

```
                    ┌─────────────────────────────────────────────────────────┐
                    │              Sistema Distribuido EcDistri2026            │
                    │                                                         │
  ┌──────────┐      │  ┌─────────────┐    pedidoRegistradoEvent               │
  │  Cliente │      │  │  EcPedidos  │──────────────────────────┐            │
  │   HTTP   │      │  │  (Producer) │                          ▼            │
  └────┬─────┘      │  └─────────────┘                  ┌─────────────┐      │
       │            │                                    │  RabbitMQ   │      │
       ▼            │  ┌─────────────┐                  │    Queue    │      │
  ┌─────────────┐   │  │ API Gateway │                  └──────┬──────┘      │
  │ API Gateway │──▶│  │   (Kong)    │                         │             │
  │   (Kong)    │   │  └──────┬──────┘                         ▼             │
  └─────────────┘   │         │                       ┌─────────────────┐    │
                    │         ▼                        │  ecfact-worker  │    │
                    │  ┌──────────────┐                │  (consumer.py)  │    │
                    │  │  ecfact-api  │                └────────┬────────┘    │
                    │  │  (FastAPI)   │                         │             │
                    │  └──────┬───────┘                         │             │
                    │         │                                 │             │
                    │         └─────────────────┬───────────────┘             │
                    │                           ▼                             │
                    │                  ┌──────────────────┐                  │
                    │                  │    ecfact-db      │                  │
                    │                  │  (PostgreSQL:5434)│                  │
                    │                  └──────────────────┘                  │
                    └─────────────────────────────────────────────────────────┘
```

> **📝 Completar:** Reemplace el diagrama ASCII por el diagrama real del proyecto si cuenta con uno gráfico, y describa el flujo de datos entre componentes.

---

## 3. Configuración con Docker

Docker encapsula la aplicación y sus dependencias en contenedores ligeros y reproducibles. A continuación se describen los pasos para levantar el entorno completo del módulo EcFacturas.

### 3.1 Requisitos previos

- [ ] Docker Desktop instalado y en ejecución
- [ ] Docker Compose v2 o superior
- [ ] Python 3.13 (para ejecución local sin Docker)
- [ ] Acceso a los archivos de configuración del proyecto
- [ ] RabbitMQ disponible (contenedor o instancia externa)

### 3.2 Variables de entorno

Las variables de conexión se definen en `app/core/config.py`. Para un despliegue en Docker, estas deben externalizarse como variables de entorno o en un archivo `.env`.

| Variable | Descripción | Valor de ejemplo |
|---|---|---|
| `DATABASE_URL` | Cadena completa de conexión PostgreSQL | `postgresql+psycopg2://postgres:admin@ecfact-db:5432/EcFacturas` |
| `RABBITMQ_HOST` | Host del broker RabbitMQ | `ecfact-rabbitmq` |
| `RABBITMQ_PORT` | Puerto AMQP de RabbitMQ | `5672` |
| `RABBITMQ_USER` | Usuario RabbitMQ | `admin` |
| `RABBITMQ_PASS` | Contraseña RabbitMQ | `****` |
| `RABBITMQ_QUEUE` | Nombre de la cola a escuchar | `pedidoRegistradoEvent` |
| `API_PORT` | Puerto expuesto por la API FastAPI | `8001` |

### 3.3 Archivo `docker-compose.yml`

El archivo `docker-compose.yml` define los servicios, redes y volúmenes necesarios para el módulo EcFacturas:

| Servicio | Nombre del contenedor | Rol |
|---|---|---|
| API REST | `ecfact-api` | Endpoints CRUD de facturas y pedidos |
| Worker RabbitMQ | `ecfact-worker` | Consumidor del evento `pedidoRegistradoEvent` |
| Base de datos | `ecfact-db` | Persistencia en PostgreSQL |
| Broker de mensajes | `ecfact-rabbitmq` | Comunicación asíncrona entre microservicios |

> **📷 Insertar:** Captura o bloque de código con el contenido real del `docker-compose.yml`.

```yaml
# Reemplace este bloque con su docker-compose.yml real
version: "3.9"
services:
  ecfact-api:
    build: .
    command: uvicorn main_api:app --host 0.0.0.0 --port 8001
    ports:
      - "8001:8001"
    environment:
      - DATABASE_URL=postgresql+psycopg2://postgres:admin@ecfact-db:5432/EcFacturas
      - RABBITMQ_HOST=ecfact-rabbitmq
    depends_on:
      - ecfact-db
      - ecfact-rabbitmq

  ecfact-worker:
    build: .
    command: python main_worker.py
    environment:
      - DATABASE_URL=postgresql+psycopg2://postgres:admin@ecfact-db:5432/EcFacturas
      - RABBITMQ_HOST=ecfact-rabbitmq
    depends_on:
      - ecfact-db
      - ecfact-rabbitmq

  ecfact-db:
    image: postgres:15
    environment:
      POSTGRES_DB: EcFacturas
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: admin
    ports:
      - "5434:5432"
    volumes:
      - ecfact_data:/var/lib/postgresql/data

  ecfact-rabbitmq:
    image: rabbitmq:3-management
    ports:
      - "5672:5672"
      - "15672:15672"
    environment:
      RABBITMQ_DEFAULT_USER: admin
      RABBITMQ_DEFAULT_PASS: admin

volumes:
  ecfact_data:
```

### 3.4 Proceso de levantamiento

**Paso 1 — Construir e iniciar todos los contenedores:**

```bash
docker-compose up --build -d
```

**Paso 2 — Verificar que todos los servicios estén activos:**

```bash
docker ps
```

**Paso 3 — Consultar logs de un servicio específico:**

```bash
# Logs de la API
docker logs ecfact-api --follow

# Logs del Worker (consumidor de eventos)
docker logs ecfact-worker --follow
```

**Paso 4 — Ejecución local sin Docker (desarrollo):**

```bash
# Crear y activar entorno virtual
py -3.13 -m venv myenv
myenv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar API (Code-First crea las tablas automáticamente)
uvicorn main_api:app --reload --port 8001

# Ejecutar Worker (en otra terminal)
python main_worker.py
```

**Paso 5 — Detener el entorno:**

```bash
docker-compose down
```

---

## 4. Evidencias de Despliegue

A continuación se presentan las capturas de pantalla que evidencian el correcto funcionamiento del entorno desplegado.

### 4.1 Docker Desktop / RabbitMQ funcionando

> **📷 Insertar:** Captura de Docker Desktop activo mostrando los contenedores del módulo EcFacturas, o bien la consola de administración de RabbitMQ en `http://localhost:15672`.

---

### 4.2 Contenedores activos

> **📷 Insertar:** Captura de la salida de `docker ps` o de la vista de contenedores en Docker Desktop.

Salida esperada de `docker ps`:

```
CONTAINER ID   IMAGE             COMMAND                  STATUS         PORTS                      NAMES
xxxxxxxxxxxx   ecfact-api        "uvicorn main_api:..."   Up 2 minutes   0.0.0.0:8001->8001/tcp     ecfact-api
xxxxxxxxxxxx   ecfact-worker     "python main_worke..."   Up 2 minutes                              ecfact-worker
xxxxxxxxxxxx   postgres:15       "docker-entrypoint..."   Up 2 minutes   0.0.0.0:5434->5432/tcp     ecfact-db
xxxxxxxxxxxx   rabbitmq:3-mgmt   "docker-entrypoint..."   Up 2 minutes   0.0.0.0:5672->5672/tcp     ecfact-rabbitmq
```

---

### 4.3 Base de datos y tablas creadas (Code-First)

> **📷 Insertar:** Captura de las tablas `pedido` y `factura` creadas en PostgreSQL (desde DBeaver, pgAdmin u otro cliente de base de datos), mostrando la estructura de columnas.

Las tablas son generadas automáticamente por SQLAlchemy al iniciar la API mediante:

```python
# main_api.py
Base.metadata.create_all(bind=engine)
```

---

### 4.4 Cola RabbitMQ activa

> **📷 Insertar:** Captura de la consola de administración de RabbitMQ (`http://localhost:15672`) mostrando la cola `pedidoRegistradoEvent` activa y el Worker conectado como consumidor.

---

### 4.5 Endpoints funcionando

#### Swagger UI

> **📷 Insertar:** Captura de Swagger UI (`http://localhost:8001/docs`) mostrando los grupos de endpoints `facturas`, `pedidos` y `seguridad`.

#### Prueba con Postman — Login (obtener JWT)

> **📷 Insertar:** Captura de la petición `POST /login` ejecutada desde Postman con las credenciales `admin@gmail.com` / `admin` y la respuesta con el token JWT.

#### Prueba con Postman — CRUD de Facturas

> **📷 Insertar:** Captura de una petición `GET /facturas` con el header `Authorization: Bearer <token>` y la lista de facturas en la respuesta.

#### Worker — Generación automática de factura

> **📷 Insertar:** Captura de los logs del Worker (`ecfact-worker`) mostrando la recepción del evento `pedidoRegistradoEvent` y la generación exitosa de la factura.

---

## 5. Referencia del CRUD

Las operaciones CRUD gestionan los recursos del módulo a través de los endpoints RESTful expuestos por la API FastAPI. La autenticación mediante JWT Bearer Token es requerida en los endpoints marcados con 🔒.

### 5.1 Autenticación

| Método HTTP | Endpoint | Auth | Descripción |
|---|---|---|---|
| `POST` | `/login` | ❌ | Obtiene un token JWT con credenciales válidas |

**Credenciales de prueba:** `admin@gmail.com` / `admin`

**Respuesta:**
```json
"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

---

### 5.2 Entidad: `Factura`

| Método HTTP | Endpoint | Auth | Descripción |
|---|---|---|---|
| `GET` | `/facturas` | 🔒 JWT | Obtiene la lista de todas las facturas registradas |
| `GET` | `/facturas/{id}` | ❌ | Obtiene los datos de una factura por su ID |
| `POST` | `/facturas` | 🔒 JWT | Crea una nueva factura manualmente en el sistema |
| `PUT` | `/facturas/{id}` | ❌ | Actualiza los datos de una factura existente |
| `DELETE` | `/facturas/{id}` | ❌ | Elimina una factura por su ID |

#### Modelo SQLAlchemy — `Factura`

```python
class Factura(Base):
    __tablename__ = "factura"

    id             = Column(Integer, primary_key=True, autoincrement=True)
    pedido_id      = Column(Integer, ForeignKey("pedido.id"), nullable=False)
    numero_factura = Column(String(50), unique=True, nullable=False)
    fecha_factura  = Column(DateTime, nullable=False)
    total_factura  = Column(Numeric(10, 2), nullable=False)
```

#### DTO JSON — Solicitud `FacturaCreate`

```json
{
  "pedido_id": 15,
  "numero_factura": "FAC-20260509-15",
  "fecha_factura": "2026-05-09T14:20:00",
  "total_factura": 32.25
}
```

#### DTO JSON — Respuesta `FacturaResponse`

```json
{
  "id": 1,
  "pedido_id": 15,
  "numero_factura": "FAC-20260509-15",
  "fecha_factura": "2026-05-09T14:20:00",
  "total_factura": 32.25
}
```

> **📝 Completar:** Ajuste los campos del modelo según la entidad real final de su proyecto si hubo cambios posteriores.

---

### 5.3 Entidad: `Pedido` (solo consulta)

Los pedidos son persistidos automáticamente por el Worker al recibir el evento de RabbitMQ. Los endpoints de pedido están disponibles únicamente para **consulta**; la creación/modificación de pedidos es responsabilidad del módulo `EcPedidos`.

| Método HTTP | Endpoint | Auth | Descripción |
|---|---|---|---|
| `GET` | `/pedidos` | 🔒 JWT | Lista todos los pedidos persistidos en EcFacturas |
| `GET` | `/pedidos/{id}` | ❌ | Obtiene los datos de un pedido por su ID |

#### Modelo SQLAlchemy — `Pedido`

```python
class Pedido(Base):
    __tablename__ = "pedido"

    id                   = Column(Integer, primary_key=True, autoincrement=False)
    direccion_cliente_id = Column(Integer, nullable=False)
    cliente_id           = Column(Integer, nullable=False)
    nombre_cliente       = Column(String(255), nullable=False)
    correo_cliente       = Column(String(255), nullable=False)
    fecha_pedido         = Column(DateTime, nullable=False)
    total_pedido         = Column(Numeric(10, 2), nullable=False)
```

#### DTO JSON — Respuesta `PedidoResponse`

```json
{
  "id": 15,
  "direccion_cliente_id": 3,
  "cliente_id": 2,
  "nombre_cliente": "Josue Proaño",
  "correo_cliente": "josue@proano.com",
  "fecha_pedido": "2026-05-09T06:28:58",
  "total_pedido": 32.25
}
```

---

## 6. Flujo del Worker RabbitMQ

Esta sección documenta el componente más relevante y diferenciador del módulo EcFacturas: el **Worker** que actúa como consumidor de eventos.

### 6.1 Descripción del flujo

```
EcPedidos (Producer)
        │
        │  Publica mensaje JSON en cola
        ▼
  ┌───────────────┐
  │   RabbitMQ    │  Cola: pedidoRegistradoEvent (durable=True)
  └───────┬───────┘
          │  Entrega mensaje al consumidor
          ▼
  ┌─────────────────────┐
  │  consumer.py        │
  │  (callback)         │
  │  1. Parsea JSON     │
  │  2. Persiste Pedido │
  │  3. Genera Factura  │
  └─────────────────────┘
          │
          ▼
  ┌──────────────────┐
  │   PostgreSQL     │
  │  tabla: pedido   │
  │  tabla: factura  │
  └──────────────────┘
```

### 6.2 Evento de entrada — `pedidoRegistradoEvent`

Mensaje JSON recibido desde la cola RabbitMQ publicado por `EcPedidos`:

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

### 6.3 Resultado automático generado

Registro insertado en la tabla `factura` tras procesar el evento:

```json
{
  "id": 1,
  "pedido_id": 15,
  "numero_factura": "FAC-20260509-15",
  "fecha_factura": "2026-05-09T14:20:00",
  "total_factura": 32.25
}
```

> **Nota:** El `numero_factura` se genera automáticamente con el formato `FAC-YYYYMMDD-{pedido_id}` mediante la lógica en `factura_service.py → create_from_pedido()`.

### 6.4 Logs del Worker en operación normal

```
🚀 Iniciando suscriptor RabbitMQ - EcFacturas Worker...
   Cola: pedidoRegistradoEvent
📡 Escuchando cola pedidoRegistradoEvent...
📥 Evento recibido - pedidoRegistradoEvent: {"pedido_id": 15, ...}
✅ Pedido 15 persistido y factura generada: FAC-20260509-15
```

---

## 7. Conclusiones

> **📝 Completar:** Reemplace cada punto con sus reflexiones reales al concluir el módulo.

- **[C1]** _(Arquitectura Event-Driven)_ — Reflexione sobre cómo la comunicación asíncrona mediante RabbitMQ desacopla los módulos `EcPedidos` y `EcFacturas`, y las ventajas que esto aporta en escalabilidad y tolerancia a fallos.
- **[C2]** _(Python + FastAPI)_ — Evalúe la experiencia de desarrollar una API REST con FastAPI en comparación con otros frameworks, destacando características como la generación automática de Swagger UI y la validación con Pydantic.
- **[C3]** _(Code-First con SQLAlchemy)_ — Describa cómo el enfoque Code-First simplifica la gestión del esquema de base de datos al generar las tablas automáticamente desde los modelos Python.
- **[C4]** _(Worker como microservicio independiente)_ — Reflexione sobre el diseño de tener el Worker (`main_worker.py`) como proceso separado de la API (`main_api.py`) y cómo esto favorece la responsabilidad única.
- **[C5]** _(Desafíos y soluciones)_ — Describa los obstáculos encontrados durante el despliegue (por ejemplo, mapeo del evento snake_case, autenticación JWT) y cómo fueron resueltos.
- **[C6]** _(Valor académico-profesional)_ — Exponga el valor de esta práctica para su formación como desarrollador de software en arquitecturas distribuidas reales.

---

## 8. Referencias

- FastAPI. (2024). *FastAPI Documentation*. https://fastapi.tiangolo.com
- SQLAlchemy. (2024). *SQLAlchemy Documentation*. https://docs.sqlalchemy.org
- RabbitMQ. (2024). *RabbitMQ Documentation*. https://www.rabbitmq.com/documentation.html
- Pika. (2024). *Pika — Python RabbitMQ Client*. https://pika.readthedocs.io
- PostgreSQL. (2024). *PostgreSQL Documentation*. https://www.postgresql.org/docs
- Docker Inc. (2024). *Docker Documentation*. https://docs.docker.com
- > **📝 Completar:** Agregue las referencias bibliográficas adicionales utilizadas en formato APA o IEEE.

---

<sub>Instituto Superior Universitario Japón · Aplicaciones Distribuidas · 2026</sub>
