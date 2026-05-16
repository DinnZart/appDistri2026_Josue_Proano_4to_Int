# 🏛️ Informe Técnico — Configuración de API Gateway con Kong

---

## 📋 Portada

| Campo | Detalle |
|---|---|
| **Estudiante** | Josue Ismael Proaño Arroyo |
| **Curso** | 4to - Desarrollo de Software |
| **Fecha** | 15/05/2026 |
| **Docente** | Ing. Geovanny Colcha |
| **Asignatura** | Aplicaciones Distribuidas |
| **Tema** | Configuración de API Gateway Kong — Integración de Microservicios |

---

## 1. Introducción

El presente informe documenta el proceso completo de instalación, configuración y pruebas del **API Gateway Kong**, utilizado como punto de entrada centralizado para los tres microservicios del ecosistema de e-commerce:

| Servicio | Tecnología | Puerto Nativo | Base de Datos |
|---|---|---|---|
| **EcCliente** | ASP.NET Core (C#) | `5180` | SQL Server (puerto `1434`) |
| **EcPedidos** | FastAPI (Python) | `8000` | MySQL (puerto `3307`) |
| **EcFacturación** | FastAPI (Python) | `8001` | PostgreSQL (puerto `5434`) |

Kong actúa como **proxy inverso inteligente**, redirigiendo las peticiones del cliente hacia el microservicio correcto según la ruta solicitada, centralizando la gestión de rutas, seguridad y monitoreo.

---

## 2. Arquitectura General del Sistema

```
┌──────────────────────────────────────────────────────────────────┐
│                        CLIENTE (Postman)                        │
│                     http://localhost:8000                        │
└──────────────────────┬───────────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────────┐
│                    KONG API GATEWAY (:8000)                      │
│                                                                  │
│  ┌────────────────┐ ┌────────────────┐ ┌──────────────────────┐  │
│  │ Route /cliente │ │ Route /pedidos │ │ Route /facturacion   │  │
│  └───────┬────────┘ └───────┬────────┘ └──────────┬───────────┘  │
└──────────┼──────────────────┼─────────────────────┼──────────────┘
           │                  │                     │
           ▼                  ▼                     ▼
  ┌────────────────┐ ┌────────────────┐  ┌──────────────────────┐
  │  EcCliente API │ │ EcPedidos API  │  │  EcFacturación API   │
  │  .NET Core     │ │  FastAPI       │  │  FastAPI             │
  │  :5180         │ │  :8000         │  │  :8001               │
  └────────┬───────┘ └───────┬────────┘  └──────────┬───────────┘
           │                  │                      │
           ▼                  ▼                      ▼
  ┌────────────────┐ ┌────────────────┐  ┌──────────────────────┐
  │  SQL Server    │ │  MySQL         │  │  PostgreSQL          │
  │  :1434         │ │  :3307         │  │  :5434               │
  └────────────────┘ └────────────────┘  └──────────────────────┘
```

> **Nota:** Los tres servicios también se comunican entre sí mediante **RabbitMQ** (puerto `5672`) para eventos asíncronos como `clienteDireccionEvent` y `pedidoRegistradoEvent`.

---

## 3. Análisis de Endpoints por Servicio

### 3.1 EcCliente (ASP.NET Core — Puerto 5180)

Base URL nativa: `http://localhost:5180`

#### 3.1.1 ClienteController — `api/Cliente`

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/api/Cliente` | Mensaje de prueba "Hola Mundo" |
| `GET` | `/api/Cliente/obtener-todos` | Obtener todos los clientes |
| `GET` | `/api/Cliente/{id}` | Obtener cliente por ID |
| `POST` | `/api/Cliente` | Crear nuevo cliente |
| `PUT` | `/api/Cliente/{id}` | Actualizar cliente |
| `DELETE` | `/api/Cliente/{id}` | Eliminar cliente |

**Modelo ClienteDTO:**
```json
{
  "id": 0,
  "estado": true,
  "nombre": "string",
  "apellido": "string",
  "email": "string",
  "cedulaIdentidad": "string (max 10)",
  "fechaNacimiento": "2026-01-01T00:00:00",
  "telefono": "string"
}
```

#### 3.1.2 DireccionClienteController — `api/DireccionCliente`

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/api/DireccionCliente/obtener-todos` | Obtener todas las direcciones |
| `GET` | `/api/DireccionCliente/{id}` | Obtener dirección por ID |
| `POST` | `/api/DireccionCliente` | Registrar dirección |
| `PUT` | `/api/DireccionCliente/{id}` | Actualizar dirección |
| `DELETE` | `/api/DireccionCliente/{id}` | Eliminar dirección |

**Modelo DireccionClienteDTO:**
```json
{
  "id": 0,
  "clienteId": 0,
  "provincia": "string",
  "ciudad": "string",
  "direccion": "string",
  "codigoPostal": "string",
  "estado": true
}
```

---

### 3.2 EcPedidos (FastAPI Python — Puerto 8000)

Base URL nativa: `http://localhost:8000`

#### Endpoints de Pedidos — `/pedidos`

| Método | Ruta | Descripción | Auth JWT |
|---|---|---|---|
| `GET` | `/pedidos` | Obtener todos los pedidos | ✅ Sí |
| `GET` | `/pedidos/{id}` | Obtener pedido por ID | ❌ No |
| `POST` | `/pedidos` | Registrar nuevo pedido | ✅ Sí |
| `PUT` | `/pedidos/{id}` | Actualizar pedido | ❌ No |
| `DELETE` | `/pedidos/{id}` | Eliminar pedido | ❌ No |

#### Endpoint de Login — `/login`

| Método | Ruta | Descripción |
|---|---|---|
| `POST` | `/login` | Obtener token JWT |

**Credenciales:** `email: admin@gmail.com` / `password: admin`

**Modelo PedidoCreate:**
```json
{
  "direccion_cliente_id": 1,
  "fecha_pedido": "2026-05-15T00:00:00",
  "total": 150.50
}
```

---

### 3.3 EcFacturación (FastAPI Python — Puerto 8001)

Base URL nativa: `http://localhost:8001`

#### 3.3.1 Endpoints de Facturas — `/facturas`

| Método | Ruta | Descripción | Auth JWT |
|---|---|---|---|
| `GET` | `/facturas` | Obtener todas las facturas | ✅ Sí |
| `GET` | `/facturas/{id}` | Obtener factura por ID | ❌ No |
| `POST` | `/facturas` | Registrar nueva factura | ✅ Sí |
| `PUT` | `/facturas/{id}` | Actualizar factura | ❌ No |
| `DELETE` | `/facturas/{id}` | Eliminar factura | ❌ No |

#### 3.3.2 Endpoints de Pedidos (consulta) — `/pedidos`

| Método | Ruta | Descripción | Auth JWT |
|---|---|---|---|
| `GET` | `/pedidos` | Consultar pedidos replicados | ✅ Sí |
| `GET` | `/pedidos/{id}` | Consultar pedido por ID | ❌ No |

#### Endpoint de Login — `/login`

| Método | Ruta | Descripción |
|---|---|---|
| `POST` | `/login` | Obtener token JWT |

**Modelo FacturaCreate:**
```json
{
  "pedido_id": 1,
  "numero_factura": "FAC-001",
  "fecha_factura": "2026-05-15T00:00:00",
  "total_factura": 150.50
}
```

---

## 4. Instalación de Kong con Docker

### 4.1 Prerrequisitos

- **Docker Desktop** instalado y funcionando en Windows.
- Verificar con:
```bash
docker --version
docker-compose --version
```

### 4.2 Archivo `docker-compose.yml`

Crear el archivo `docker-compose.yml` en la raíz del proyecto:

```yaml
version: "3.9"

networks:
  kong-net:
    driver: bridge

services:
  # =============================================
  # Base de Datos de Kong (PostgreSQL)
  # =============================================
  kong-database:
    image: postgres:13
    container_name: kong-database
    restart: always
    networks:
      - kong-net
    environment:
      POSTGRES_USER: kong
      POSTGRES_DB: kong
      POSTGRES_PASSWORD: kongpass
    ports:
      - "5433:5432"
    volumes:
      - kong-db-data:/var/lib/postgresql/data

  # =============================================
  # Migración de la BD de Kong
  # =============================================
  kong-migration:
    image: kong:3.6
    container_name: kong-migration
    networks:
      - kong-net
    depends_on:
      - kong-database
    environment:
      KONG_DATABASE: postgres
      KONG_PG_HOST: kong-database
      KONG_PG_USER: kong
      KONG_PG_PASSWORD: kongpass
    command: kong migrations bootstrap
    restart: on-failure

  # =============================================
  # Kong API Gateway
  # =============================================
  kong:
    image: kong:3.6
    container_name: kong
    restart: always
    networks:
      - kong-net
    depends_on:
      - kong-database
      - kong-migration
    environment:
      KONG_DATABASE: postgres
      KONG_PG_HOST: kong-database
      KONG_PG_USER: kong
      KONG_PG_PASSWORD: kongpass
      KONG_PROXY_ACCESS_LOG: /dev/stdout
      KONG_ADMIN_ACCESS_LOG: /dev/stdout
      KONG_PROXY_ERROR_LOG: /dev/stderr
      KONG_ADMIN_ERROR_LOG: /dev/stderr
      KONG_ADMIN_LISTEN: 0.0.0.0:8001
    ports:
      - "8080:8000"   # Puerto proxy (peticiones del cliente)
      - "8443:8443"   # Puerto proxy HTTPS
      - "8001:8001"   # Puerto Admin API
      - "8444:8444"   # Puerto Admin API HTTPS
    healthcheck:
      test: ["CMD", "kong", "health"]
      interval: 10s
      timeout: 10s
      retries: 10

volumes:
  kong-db-data:
```

> **⚠️ Importante:** Se usa el puerto `8080` para el proxy de Kong (en lugar del `8000` por defecto) para evitar conflicto con el servicio EcPedidos que ya usa el puerto `8000`. El puerto Admin API de Kong (`8001`) también puede entrar en conflicto con EcFacturación — ajustar según sea necesario (ej. mapear a `8002`).

### 4.3 Levantar los Contenedores

```bash
# Levantar todos los contenedores
docker-compose up -d

# Verificar que estén activos
docker ps
```

**Contenedores esperados:**

| Contenedor | Imagen | Puerto |
|---|---|---|
| `kong` | `kong:3.6` | `8080`, `8001` |
| `kong-database` | `postgres:13` | `5433` |

### 4.4 Verificar que Kong está activo

```bash
curl -i http://localhost:8001/
```

Debe retornar un JSON con la información de Kong (versión, plugins disponibles, etc.).

> 📸 **Captura recomendada:** Terminal mostrando `docker ps` con los contenedores activos.

---

## 5. Configuración de Servicios y Rutas en Kong

Se utiliza la **Admin API de Kong** (puerto `8001`) para registrar cada microservicio y sus rutas. Dado que los servicios corren en la máquina host (no en Docker), se usa `host.docker.internal` como hostname.

### 5.1 Servicio EcCliente

#### Registrar el Servicio

```bash
curl -i -X POST http://localhost:8001/services/ \
  --data "name=eccliente-service" \
  --data "url=http://host.docker.internal:5180"
```

#### Registrar la Ruta

```bash
curl -i -X POST http://localhost:8001/services/eccliente-service/routes \
  --data "name=eccliente-route" \
  --data "paths[]=/cliente" \
  --data "strip_path=true"
```

> Con `strip_path=true`, una petición a `http://localhost:8080/cliente/api/Cliente/obtener-todos` se reenvía a `http://host.docker.internal:5180/api/Cliente/obtener-todos`.

---

### 5.2 Servicio EcPedidos

#### Registrar el Servicio

```bash
curl -i -X POST http://localhost:8001/services/ \
  --data "name=ecpedidos-service" \
  --data "url=http://host.docker.internal:8000"
```

#### Registrar la Ruta

```bash
curl -i -X POST http://localhost:8001/services/ecpedidos-service/routes \
  --data "name=ecpedidos-route" \
  --data "paths[]=/pedidos" \
  --data "strip_path=false"
```

> Con `strip_path=false`, la ruta `/pedidos` se preserva y se reenvía tal cual al servicio FastAPI, que espera recibir `/pedidos` directamente.

---

### 5.3 Servicio EcFacturación

#### Registrar el Servicio

```bash
curl -i -X POST http://localhost:8001/services/ \
  --data "name=ecfacturacion-service" \
  --data "url=http://host.docker.internal:8001"
```

> **Nota:** Si el puerto Admin de Kong también es `8001`, cambiar el mapeo de Kong en el `docker-compose.yml` (ej. `8002:8001`) para evitar conflicto.

#### Registrar la Ruta

```bash
curl -i -X POST http://localhost:8001/services/ecfacturacion-service/routes \
  --data "name=ecfacturacion-route" \
  --data "paths[]=/facturacion" \
  --data "strip_path=true"
```

---

### 5.4 Verificar Servicios y Rutas Registrados

```bash
# Listar servicios
curl -s http://localhost:8001/services | python -m json.tool

# Listar rutas
curl -s http://localhost:8001/routes | python -m json.tool
```

> 📸 **Capturas recomendadas:**
> - Respuesta de creación de cada servicio
> - Respuesta de creación de cada ruta
> - Listado de servicios y rutas registrados

---

## 6. Ruteo de Endpoints a través de Kong

A continuación se muestra la tabla completa de endpoints accesibles a través del proxy de Kong (puerto `8080`).

### 6.1 Cliente (vía Kong → EcCliente API)

| Método | URL a través de Kong | Destino real |
|---|---|---|
| `GET` | `http://localhost:8080/cliente/api/Cliente/obtener-todos` | `http://localhost:5180/api/Cliente/obtener-todos` |
| `GET` | `http://localhost:8080/cliente/api/Cliente/{id}` | `http://localhost:5180/api/Cliente/{id}` |
| `POST` | `http://localhost:8080/cliente/api/Cliente` | `http://localhost:5180/api/Cliente` |
| `PUT` | `http://localhost:8080/cliente/api/Cliente/{id}` | `http://localhost:5180/api/Cliente/{id}` |
| `DELETE` | `http://localhost:8080/cliente/api/Cliente/{id}` | `http://localhost:5180/api/Cliente/{id}` |

### 6.2 Dirección Cliente (vía Kong → EcCliente API)

| Método | URL a través de Kong | Destino real |
|---|---|---|
| `GET` | `http://localhost:8080/cliente/api/DireccionCliente/obtener-todos` | `http://localhost:5180/api/DireccionCliente/obtener-todos` |
| `GET` | `http://localhost:8080/cliente/api/DireccionCliente/{id}` | `http://localhost:5180/api/DireccionCliente/{id}` |
| `POST` | `http://localhost:8080/cliente/api/DireccionCliente` | `http://localhost:5180/api/DireccionCliente` |
| `PUT` | `http://localhost:8080/cliente/api/DireccionCliente/{id}` | `http://localhost:5180/api/DireccionCliente/{id}` |
| `DELETE` | `http://localhost:8080/cliente/api/DireccionCliente/{id}` | `http://localhost:5180/api/DireccionCliente/{id}` |

### 6.3 Pedidos (vía Kong → EcPedidos API)

| Método | URL a través de Kong | Destino real | JWT |
|---|---|---|---|
| `POST` | `http://localhost:8080/pedidos/login` | `http://localhost:8000/login` | — |
| `GET` | `http://localhost:8080/pedidos` | `http://localhost:8000/pedidos` | ✅ |
| `GET` | `http://localhost:8080/pedidos/{id}` | `http://localhost:8000/pedidos/{id}` | ❌ |
| `POST` | `http://localhost:8080/pedidos` | `http://localhost:8000/pedidos` | ✅ |
| `PUT` | `http://localhost:8080/pedidos/{id}` | `http://localhost:8000/pedidos/{id}` | ❌ |
| `DELETE` | `http://localhost:8080/pedidos/{id}` | `http://localhost:8000/pedidos/{id}` | ❌ |

### 6.4 Facturación (vía Kong → EcFacturación API)

| Método | URL a través de Kong | Destino real | JWT |
|---|---|---|---|
| `POST` | `http://localhost:8080/facturacion/login` | `http://localhost:8001/login` | — |
| `GET` | `http://localhost:8080/facturacion/facturas` | `http://localhost:8001/facturas` | ✅ |
| `GET` | `http://localhost:8080/facturacion/facturas/{id}` | `http://localhost:8001/facturas/{id}` | ❌ |
| `POST` | `http://localhost:8080/facturacion/facturas` | `http://localhost:8001/facturas` | ✅ |
| `PUT` | `http://localhost:8080/facturacion/facturas/{id}` | `http://localhost:8001/facturas/{id}` | ❌ |
| `DELETE` | `http://localhost:8080/facturacion/facturas/{id}` | `http://localhost:8001/facturas/{id}` | ❌ |

---

## 7. Pruebas en Postman

### 7.1 Configuración Previa

1. Crear una **Collection** en Postman llamada `Kong API Gateway Tests`.
2. Crear carpetas: `EcCliente`, `EcPedidos`, `EcFacturación`.
3. Para servicios con JWT, primero obtener el token vía `/login`.

### 7.2 Obtener Token JWT (EcPedidos / EcFacturación)

**Request:**
```
POST http://localhost:8080/pedidos/login
Content-Type: application/json

{
  "email": "admin@gmail.com",
  "password": "admin"
}
```

**Response esperada:** Un token JWT string.

Copiar el token y usarlo en las peticiones protegidas con el header:
```
Authorization: Bearer <token>
```

### 7.3 Ejemplo — GET Todos los Clientes

```
GET http://localhost:8080/cliente/api/Cliente/obtener-todos
```

**Response esperada (200 OK):**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "nombre": "Juan",
      "apellido": "Pérez",
      "email": "juan@mail.com",
      "cedulaIdentidad": "1234567890",
      "fechaNacimiento": "1995-03-15T00:00:00",
      "telefono": "0991234567",
      "estado": true
    }
  ]
}
```

### 7.4 Ejemplo — POST Crear Cliente

```
POST http://localhost:8080/cliente/api/Cliente
Content-Type: application/json

{
  "nombre": "María",
  "apellido": "López",
  "email": "maria@mail.com",
  "cedulaIdentidad": "0987654321",
  "fechaNacimiento": "1998-07-20T00:00:00",
  "telefono": "0997654321",
  "estado": true
}
```

### 7.5 Ejemplo — PUT Actualizar Pedido

```
PUT http://localhost:8080/pedidos/1
Content-Type: application/json

{
  "direccion_cliente_id": 1,
  "fecha_pedido": "2026-05-15T10:00:00",
  "total": 200.00
}
```

### 7.6 Ejemplo — DELETE Eliminar Factura

```
DELETE http://localhost:8080/facturacion/facturas/1
```

**Response esperada (200 OK):**
```json
{
  "message": "Factura eliminada correctamente"
}
```

### 7.7 Ejemplo — POST Crear Factura (con JWT)

```
POST http://localhost:8080/facturacion/facturas
Content-Type: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6...

{
  "pedido_id": 1,
  "numero_factura": "FAC-001",
  "fecha_factura": "2026-05-15T00:00:00",
  "total_factura": 150.50
}
```

> 📸 **Capturas recomendadas por cada servicio:**
> - GET todos (200 OK con datos)
> - GET por ID (200 OK con un registro)
> - POST crear (200/201 OK con registro creado)
> - PUT actualizar (200 OK con registro actualizado)
> - DELETE eliminar (200 OK con mensaje de confirmación)
> - Login para obtener JWT (si aplica)

---

## 8. Explicación del Ruteo en API Gateway

### ¿Cómo funciona el ruteo en Kong?

Kong opera como un **proxy inverso** que intercepta todas las peticiones entrantes en su puerto proxy (`8080`) y las redirige al servicio backend correspondiente según las reglas de ruteo configuradas.

El flujo es:

```
1. Cliente envía petición → http://localhost:8080/cliente/api/Cliente/obtener-todos
2. Kong recibe la petición en el puerto proxy (8080)
3. Kong evalúa las RUTAS registradas y encuentra que /cliente coincide
4. Kong identifica el SERVICIO asociado → eccliente-service (http://host.docker.internal:5180)
5. Si strip_path=true, Kong elimina el prefijo /cliente de la URL
6. Kong reenvía la petición → http://host.docker.internal:5180/api/Cliente/obtener-todos
7. El microservicio procesa la petición y devuelve la respuesta
8. Kong retransmite la respuesta al cliente
```

### Conceptos Clave

| Concepto | Descripción |
|---|---|
| **Service** | Representa un microservicio upstream. Define el host, puerto y protocolo del backend. |
| **Route** | Define las reglas de coincidencia (paths, métodos, hosts) para dirigir tráfico a un Service. |
| **strip_path** | Si es `true`, elimina el prefijo de la ruta antes de reenviar. Si es `false`, envía la ruta completa. |
| **Upstream** | El servidor backend real que procesa las peticiones. |
| **Plugin** | Extensiones para agregar funcionalidad (autenticación, rate limiting, logging, etc.). |

### ¿Por qué usar un API Gateway?

1. **Punto de entrada único:** Un solo URL base para todos los microservicios.
2. **Desacoplamiento:** Los clientes no necesitan conocer las IPs/puertos individuales.
3. **Seguridad centralizada:** Autenticación, rate limiting y CORS en un solo lugar.
4. **Monitoreo:** Logging y métricas centralizadas de todo el tráfico.
5. **Escalabilidad:** Facilita balanceo de carga y despliegue de nuevas versiones.

---

## 9. Resumen de Puertos del Sistema

| Componente | Puerto | Descripción |
|---|---|---|
| Kong Proxy | `8080` | Punto de entrada para peticiones de clientes |
| Kong Admin API | `8001` (o `8002`) | Configuración de servicios y rutas |
| Kong DB (PostgreSQL) | `5433` | Base de datos interna de Kong |
| EcCliente API | `5180` | Microservicio de clientes (.NET) |
| EcPedidos API | `8000` | Microservicio de pedidos (FastAPI) |
| EcFacturación API | `8001` | Microservicio de facturas (FastAPI) |
| RabbitMQ | `5672` | Mensajería entre microservicios |
| SQL Server | `1434` | BD de EcCliente |
| MySQL | `3307` | BD de EcPedidos |
| PostgreSQL | `5434` | BD de EcFacturación |

---

## 10. Conclusiones

1. **Kong API Gateway** permite centralizar el acceso a múltiples microservicios heterogéneos (ASP.NET Core, FastAPI) bajo un único punto de entrada, simplificando la arquitectura desde la perspectiva del cliente.

2. La configuración mediante la **Admin API REST** de Kong es directa y reproducible, permitiendo automatizar el registro de servicios y rutas mediante scripts o herramientas como Postman.

3. El parámetro `strip_path` es fundamental para adaptar las rutas del gateway a la estructura interna de cada microservicio: se usa `true` para EcCliente y EcFacturación (que necesitan que se elimine el prefijo del gateway), y `false` para EcPedidos (cuyas rutas internas coinciden con el prefijo del gateway).

4. La integración con **Docker** facilita el despliegue de Kong y su base de datos PostgreSQL de forma aislada, sin interferir con los servicios del sistema anfitrión.

5. Los servicios que manejan **autenticación JWT** (EcPedidos y EcFacturación) funcionan transparentemente a través de Kong, ya que el gateway reenvía los headers de autorización sin modificarlos.

6. El uso de un API Gateway es una **práctica estándar en arquitecturas de microservicios**, y Kong proporciona una solución robusta, extensible y de código abierto para gestionar el tráfico, la seguridad y la observabilidad del sistema distribuido.

---

> **Documento generado como parte de la asignatura de Aplicaciones Distribuidas — ISUTJ 2026**
