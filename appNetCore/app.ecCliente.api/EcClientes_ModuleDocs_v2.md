# 📦 EcClientes — Documentación de Despliegue de Módulo

> **Proyecto:** EcClientes — Gestión de Clientes y Direcciones  
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
6. [Conclusiones](#6-conclusiones)
7. [Referencias](#7-referencias)

---

## 1. Introducción

El módulo **EcClientes** es un microservicio encargado de gestionar dos recursos principales del sistema distribuido: los **clientes** y sus **direcciones de entrega**. Su función central es exponer una API RESTful que permite crear, consultar, actualizar y eliminar estos registros de forma independiente y desacoplada del resto del sistema.

Este módulo forma parte de una arquitectura de aplicaciones distribuidas donde cada servicio tiene responsabilidad única. EcClientes se comunica con una base de datos dedicada y puede integrarse con otros módulos (pedidos, autenticación, etc.) a través del API Gateway, sin depender directamente de ellos.

**Objetivos del módulo:**

- Implementar operaciones CRUD completas sobre las entidades `Cliente` y `DireccionCliente`.
- Contenerizar la aplicación utilizando Docker para garantizar portabilidad y reproducibilidad del entorno.
- Documentar y exponer los endpoints mediante Swagger y Postman.
- Integrar el servicio con un API Gateway (Kong) para gestión centralizada del tráfico.

---

## 2. Descripción de la Arquitectura

La arquitectura del módulo EcClientes está basada en el patrón de **microservicios**, donde cada componente se ejecuta de forma independiente dentro de contenedores Docker, garantizando portabilidad, escalabilidad y facilidad de despliegue.

### 2.1 Stack tecnológico

| Capa | Tecnología |
|---|---|
| API Gateway | Kong |
| Backend / API REST | .NET (ASP.NET Core) |
| Base de datos | SQL Server |
| Documentación de API | Swagger / OpenAPI · Postman Collection |
| Orquestación | Docker Compose |

### 2.2 Cómo fluye una petición

El flujo de una solicitud es simple y lineal: el cliente HTTP (navegador, Postman, otra app) envía una petición al **API Gateway (Kong)**, que la enruta hacia la **API REST** (`eccl-api`). La API procesa la solicitud, consulta o escribe en la **base de datos** (`eccl-db`), y retorna la respuesta al cliente. Ningún componente accede directamente a la base de datos sin pasar por la API.

```
┌─────────────┐     ┌─────────────┐     ┌──────────────────┐     ┌──────────────┐
│  Cliente    │────▶│ API Gateway │────▶│  eccl-api        │────▶│   eccl-db    │
│  HTTP       │     │   (Kong)    │     │  (.NET Core)     │     │ (SQL Server) │
└─────────────┘     └─────────────┘     └──────────────────┘     └──────────────┘
```

### 2.3 Diagrama de arquitectura

> **📷 [CAPTURA 1 — Diagrama de arquitectura]**  
> *Inserta aquí una imagen del diagrama de bloques de tu sistema. Puede ser una captura de un diagrama hecho en draw.io, Lucidchart o similar, que muestre los contenedores y las conexiones entre ellos.*

---

## 3. Configuración con Docker

Docker permite empaquetar la aplicación con todas sus dependencias en contenedores que se ejecutan de la misma forma en cualquier máquina. `docker-compose` orquesta el arranque de todos los contenedores del módulo con un solo comando.

### 3.1 Requisitos previos

- [ ] Docker Desktop instalado y en ejecución
- [ ] Docker Compose v2 o superior
- [ ] Acceso al repositorio del proyecto con los archivos de configuración

### 3.2 Estructura de servicios

El archivo `docker-compose.yml` define tres servicios principales que trabajan juntos:

| Servicio | Nombre del contenedor | Rol |
|---|---|---|
| API REST | `eccl-api` | Expone los endpoints y contiene la lógica de negocio |
| Base de datos | `eccl-db` | Almacena los datos de clientes y direcciones |
| API Gateway | `eccl-gateway` | Enruta y controla el acceso a la API |

### 3.3 Archivo `docker-compose.yml`

A continuación se muestra la configuración completa del archivo de orquestación. Define los servicios, sus puertos, variables de entorno y la red interna que los comunica.

> **📷 [CAPTURA 2 — Archivo docker-compose.yml]**  
> *Inserta aquí una captura del archivo `docker-compose.yml` abierto en tu editor (VS Code), mostrando la configuración completa del servicio.*

```yaml
# docker-compose.yml — Módulo EcClientes
version: "3.9"

services:
  eccl-api:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: eccl-api
    ports:
      - "8080:8080"
    environment:
      - ConnectionStrings__DefaultConnection=Server=eccl-db;Database=EcClientesDb;User Id=sa;Password=YourStrong!Passw0rd;
    depends_on:
      - eccl-db
    networks:
      - eccl-net

  eccl-db:
    image: mcr.microsoft.com/mssql/server:2022-latest
    container_name: eccl-db
    environment:
      SA_PASSWORD: "YourStrong!Passw0rd"
      ACCEPT_EULA: "Y"
    ports:
      - "1433:1433"
    volumes:
      - eccl_data:/var/opt/mssql
    networks:
      - eccl-net

  eccl-gateway:
    image: kong:latest
    container_name: eccl-gateway
    ports:
      - "8000:8000"
      - "8001:8001"
    networks:
      - eccl-net

networks:
  eccl-net:
    driver: bridge

volumes:
  eccl_data:
```

### 3.4 Variables de entorno

Las variables de entorno configuran la conexión entre la API y la base de datos. No deben quedar expuestas en repositorios públicos; en producción se gestionan mediante un archivo `.env` o un gestor de secretos.

| Variable | Descripción | Valor de ejemplo |
|---|---|---|
| `ConnectionStrings__DefaultConnection` | Cadena completa de conexión a SQL Server | `Server=eccl-db;Database=...` |
| `SA_PASSWORD` | Contraseña del usuario `sa` en SQL Server | `YourStrong!Passw0rd` |
| `ACCEPT_EULA` | Aceptación de la licencia de SQL Server | `Y` |
| `API_PORT` | Puerto expuesto por la API | `8080` |

### 3.5 Proceso de levantamiento

Ejecuta los siguientes comandos en orden desde el directorio raíz del proyecto:

**Paso 1 — Construir e iniciar todos los contenedores:**

```bash
docker-compose up --build -d
```

> La bandera `--build` fuerza la reconstrucción de la imagen de la API. La bandera `-d` inicia los contenedores en segundo plano (modo *detached*).

**Paso 2 — Verificar que todos los servicios estén activos:**

```bash
docker ps
```

**Paso 3 — Consultar logs de la API (útil para depurar errores al inicio):**

```bash
docker logs eccl-api --follow
```

**Paso 4 — Detener y eliminar los contenedores:**

```bash
docker-compose down
```

> Agrega el flag `-v` (`docker-compose down -v`) si también deseas eliminar el volumen de datos de la base de datos.

---

## 4. Evidencias de Despliegue

Esta sección presenta las capturas que demuestran el funcionamiento correcto del entorno contenedorizado y de los endpoints de la API.

### 4.1 Docker Desktop activo

> **📷 [CAPTURA 3 — Docker Desktop]**  
> *Abre Docker Desktop y toma una captura de la pantalla principal. Debe verse que el motor Docker está **corriendo** (ícono verde o indicador "Engine running"). No es necesario que haya contenedores activos aún.*

---

### 4.2 Contenedores en ejecución

Una vez ejecutado `docker-compose up --build -d`, los tres contenedores deben aparecer con estado `Up`.

> **📷 [CAPTURA 4 — Contenedores activos en Docker Desktop]**  
> *En la pestaña "Containers" de Docker Desktop, muestra los contenedores `eccl-api`, `eccl-db` y `eccl-gateway` con estado **Running**. Asegúrate de que los puertos mapeados sean visibles en la columna "Port(s)".*

La salida esperada del comando `docker ps` es similar a la siguiente:

```
CONTAINER ID   IMAGE                   STATUS         PORTS                    NAMES
xxxxxxxxxxxx   eccl-api-image          Up 2 minutes   0.0.0.0:8080->8080/tcp   eccl-api
xxxxxxxxxxxx   mssql/server:2022       Up 2 minutes   0.0.0.0:1433->1433/tcp   eccl-db
xxxxxxxxxxxx   kong:latest             Up 2 minutes   0.0.0.0:8000->8000/tcp   eccl-gateway
```

> **📷 [CAPTURA 5 — Salida de `docker ps` en terminal]**  
> *Abre una terminal (PowerShell o CMD), ejecuta `docker ps` y toma una captura mostrando los tres contenedores activos con sus columnas de estado y puertos.*

---

### 4.3 Base de datos creada

La base de datos `EcClientesDb` se crea automáticamente al iniciar la API gracias a las migraciones de Entity Framework Core. Las tablas `Clientes` y `DireccionClientes` deben existir tras el primer arranque.

> **📷 [CAPTURA 6 — Base de datos y tablas en cliente SQL]**  
> *Conéctate a la base de datos desde Azure Data Studio, DBeaver o SQL Server Management Studio, apuntando a `localhost,1433` con usuario `sa`. Toma una captura mostrando la base de datos `EcClientesDb` expandida con sus tablas (`Clientes`, `DireccionClientes`) visibles en el árbol de objetos.*

---

### 4.4 Swagger UI — Endpoints disponibles

Swagger UI se encuentra disponible en `http://localhost:8080/swagger` una vez que el contenedor `eccl-api` está en ejecución. Muestra todos los endpoints documentados de forma interactiva.

> **📷 [CAPTURA 7 — Vista general de Swagger UI]**  
> *Abre un navegador y navega a `http://localhost:8080/swagger`. Toma una captura donde se vean los grupos de endpoints `Clientes` y `DireccionClientes` expandidos (o al menos sus títulos de sección visibles).*

---

### 4.5 Pruebas con Postman

Las siguientes pruebas verifican el funcionamiento de los endpoints principales del módulo.

#### Prueba GET — Listar clientes

> **📷 [CAPTURA 8 — GET /api/clientes en Postman]**  
> *Envía una solicitud `GET` a `http://localhost:8080/api/clientes`. Toma una captura mostrando: la URL de la petición, el código de respuesta **200 OK** y el cuerpo JSON de respuesta (puede estar vacío `[]` si no hay datos aún, lo que también es correcto).*

#### Prueba POST — Crear cliente

> **📷 [CAPTURA 9 — POST /api/clientes en Postman]**  
> *Envía una solicitud `POST` a `http://localhost:8080/api/clientes` con el cuerpo JSON del modelo de cliente (ver sección 5.1). Toma una captura mostrando el cuerpo de la petición, el código de respuesta **201 Created** y el objeto creado en la respuesta.*

#### Prueba POST — Crear dirección asociada

> **📷 [CAPTURA 10 — POST /api/direcciones en Postman]**  
> *Envía una solicitud `POST` a `http://localhost:8080/api/direcciones` asociando la dirección al `clienteId` del cliente creado anteriormente. Toma una captura del código **201 Created** y la respuesta con el objeto creado.*

#### Prueba DELETE — Eliminar registro

> **📷 [CAPTURA 11 — DELETE /api/clientes/{id} en Postman]**  
> *Envía una solicitud `DELETE` a `http://localhost:8080/api/clientes/{id}` usando el ID de un cliente existente. Toma una captura mostrando el código de respuesta **204 No Content**, que confirma la eliminación exitosa.*

---

## 5. Referencia del CRUD

Las operaciones CRUD (Create, Read, Update, Delete) gestionan los recursos del módulo a través de los endpoints RESTful expuestos por la API.

### 5.1 Entidad: `Cliente`

Un **Cliente** representa a una persona registrada en el sistema, con sus datos de contacto básicos. Es la entidad principal del módulo.

| Método HTTP | Endpoint | Descripción |
|---|---|---|
| `GET` | `/api/clientes` | Obtiene la lista de todos los clientes registrados |
| `GET` | `/api/clientes/{id}` | Obtiene los datos de un cliente específico por su ID |
| `POST` | `/api/clientes` | Registra un nuevo cliente en el sistema |
| `PUT` | `/api/clientes/{id}` | Actualiza los datos de un cliente existente |
| `DELETE` | `/api/clientes/{id}` | Elimina un cliente del sistema por su ID |

#### Modelo de datos `Cliente`

Este es el esquema JSON esperado en las solicitudes `POST` y `PUT`, y retornado en las respuestas:

```json
{
  "id": 1,
  "nombre": "Juan",
  "apellido": "Pérez",
  "correo": "juan.perez@email.com",
  "telefono": "0991234567",
  "cedula": "1712345678",
  "fechaRegistro": "2026-05-15T00:00:00",
  "estado": true
}
```

> **📷 [CAPTURA 12 — Modelo Cliente en Swagger]**  
> *En Swagger UI, expande el endpoint `POST /api/clientes` y toma una captura que muestre el **Schema** del modelo `Cliente` con todos sus campos y tipos de dato.*

---

### 5.2 Entidad: `DireccionCliente`

Una **DireccionCliente** está siempre asociada a un `Cliente` existente (relación N:1). Un cliente puede tener múltiples direcciones, pero solo una puede ser marcada como principal.

| Método HTTP | Endpoint | Descripción |
|---|---|---|
| `GET` | `/api/direcciones` | Lista todas las direcciones registradas en el sistema |
| `GET` | `/api/direcciones/{id}` | Obtiene los datos de una dirección específica por su ID |
| `GET` | `/api/direcciones/cliente/{clienteId}` | Lista todas las direcciones de un cliente en particular |
| `POST` | `/api/direcciones` | Registra una nueva dirección asociada a un cliente |
| `PUT` | `/api/direcciones/{id}` | Actualiza los datos de una dirección existente |
| `DELETE` | `/api/direcciones/{id}` | Elimina una dirección del sistema por su ID |

#### Modelo de datos `DireccionCliente`

```json
{
  "id": 1,
  "clienteId": 1,
  "calle": "Av. Amazonas N23-45",
  "ciudad": "Quito",
  "provincia": "Pichincha",
  "codigoPostal": "170143",
  "referencia": "Junto al parque",
  "esPrincipal": true
}
```

> **📷 [CAPTURA 13 — Modelo DireccionCliente en Swagger]**  
> *En Swagger UI, expande el endpoint `POST /api/direcciones` y toma una captura mostrando el **Schema** del modelo `DireccionCliente` con todos sus campos.*

---

### 5.3 Relación entre entidades

Las dos entidades tienen una relación **uno a muchos**: un `Cliente` puede tener una o varias `DireccionCliente`, pero cada dirección pertenece a un único cliente. La integridad referencial está garantizada a nivel de base de datos mediante una **clave foránea** (`clienteId`).

```
Cliente (1) ──────────────── (N) DireccionCliente
  id                               id
  nombre                           clienteId  ◀── FK
  apellido                         calle
  correo                           ciudad
  telefono                         provincia
  estado                           esPrincipal
```

---

## 6. Conclusiones

A continuación se presentan las reflexiones obtenidas tras el desarrollo y despliegue del módulo EcClientes.

- **[C1] Docker y portabilidad** — El uso de contenedores Docker elimina el problema del "funciona en mi máquina". Al contenerizar tanto la API como la base de datos, el entorno completo es reproducible en cualquier sistema con un solo comando, lo que simplifica enormemente el trabajo colaborativo y el despliegue en producción.

- **[C2] Arquitectura de microservicios** — Separar la gestión de clientes en su propio servicio permite que otros módulos del sistema distribuido dependan de él únicamente a través de su API, sin acoplamiento de código. Esto facilita escalar, mantener o reemplazar el módulo de forma independiente.

- **[C3] API RESTful con .NET Core** — La implementación de los endpoints siguió los estándares REST: verbos HTTP correctos (`GET`, `POST`, `PUT`, `DELETE`), códigos de estado apropiados (`200`, `201`, `204`, `404`) y estructura de recursos coherente (`/api/clientes`, `/api/direcciones`). Esto garantiza que la API sea predecible e intuitiva para cualquier cliente que la consuma.

- **[C4] Desafíos y soluciones** — El principal desafío fue la sincronización del inicio de la API con la disponibilidad de la base de datos. SQL Server tarda algunos segundos en estar listo tras iniciarse su contenedor, lo que causaba errores de conexión en la API. Esto se resolvió configurando la política `depends_on` con condiciones de salud (`healthcheck`) en el `docker-compose.yml`.

- **[C5] Valor académico-profesional** — Este módulo consolidó competencias clave para el perfil de un desarrollador de software moderno: diseño de APIs, manejo de contenedores, gestión de bases de datos en entornos aislados y documentación técnica. Estas habilidades son directamente aplicables en entornos de trabajo reales donde Docker y los microservicios son el estándar de la industria.

---

## 7. Referencias

- Docker Inc. (2024). *Docker Documentation*. https://docs.docker.com
- Kong Inc. (2024). *Kong Gateway Documentation*. https://docs.konghq.com
- Microsoft. (2024). *ASP.NET Core documentation*. https://learn.microsoft.com/en-us/aspnet/core
- Microsoft. (2024). *SQL Server on Linux with Docker*. https://learn.microsoft.com/en-us/sql/linux/quickstart-install-connect-docker
- Microsoft. (2024). *Entity Framework Core — Migrations*. https://learn.microsoft.com/en-us/ef/core/managing-schemas/migrations
- Fielding, R. T. (2000). *Architectural Styles and the Design of Network-based Software Architectures* (Tesis doctoral). University of California, Irvine.

---

<sub>Instituto Superior Universitario Japón · Aplicaciones Distribuidas · 2026</sub>
