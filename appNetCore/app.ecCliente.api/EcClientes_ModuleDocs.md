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

El presente documento describe el proceso de análisis, configuración y despliegue del módulo **EcClientes**, una aplicación orientada a la gestión de clientes y sus respectivas direcciones, desarrollada bajo un esquema de microservicios y contenedores mediante Docker.

> **📝 Completar:** Amplie aquí con el contexto académico, los objetivos del módulo y su relevancia dentro del sistema distribuido mayor al que pertenece EcClientes.

---

## 2. Descripción de la Arquitectura

La arquitectura del módulo EcClientes está basada en el patrón de **microservicios**, donde cada componente se ejecuta de forma independiente dentro de contenedores Docker, garantizando portabilidad, escalabilidad y facilidad de despliegue.

### 2.1 Stack tecnológico

| Capa | Tecnología |
|---|---|
| API Gateway | Kong |
| Backend / API REST | .NET · Python (FastAPI) |
| Base de datos | MySQL · PostgreSQL · SQL Server |
| Documentación de API | Swagger / OpenAPI · Postman Collection |
| Orquestación | Docker Compose |

---

## 3. Configuración con Docker

Docker encapsula la aplicación y sus dependencias en contenedores ligeros y reproducibles. A continuación se describen los pasos para levantar el entorno completo del módulo.

### 3.1 Requisitos previos

- [ ] Docker Desktop instalado y en ejecución
- [ ] Docker Compose v2 o superior
- [ ] Acceso a los archivos `.yml` de configuración del proyecto

### 3.2 Archivo `docker-compose.yml`

El archivo `docker-compose.yml` define los servicios, redes y volúmenes necesarios. Incluye como mínimo los siguientes servicios:

| Servicio | Nombre del contenedor | Rol |
|---|---|---|
| API REST | `eccl-api` | Lógica de negocio y endpoints |
| Base de datos | `eccl-db` | Persistencia de datos |
| API Gateway | `eccl-gateway` | Enrutamiento y gestión de tráfico |

> **📷 Insertar:** Captura o bloque de código con el contenido real del `docker-compose.yml`.

```yaml
# Reemplace este bloque con su docker-compose.yml real
version: "3.9"
services:
  eccl-api:
    build: .
    ports:
      - "8080:8080"
    environment:
      - DB_HOST=eccl-db
      - DB_PORT=5432
    depends_on:
      - eccl-db

  eccl-db:
    image: postgres:15
    environment:
      POSTGRES_DB: eccl_db
      POSTGRES_USER: eccl_user
      POSTGRES_PASSWORD: eccl_pass
    volumes:
      - eccl_data:/var/lib/postgresql/data

volumes:
  eccl_data:
```

### 3.3 Variables de entorno

> **📝 Completar:** Documente las variables de entorno relevantes del módulo.

| Variable | Descripción | Valor de ejemplo |
|---|---|---|
| `DB_HOST` | Host de la base de datos | `eccl-db` |
| `DB_PORT` | Puerto de la base de datos | `5432` |
| `DB_NAME` | Nombre de la base de datos | `eccl_db` |
| `DB_USER` | Usuario de la base de datos | `eccl_user` |
| `DB_PASSWORD` | Contraseña de la base de datos | `****` |
| `API_PORT` | Puerto expuesto por la API | `8080` |

### 3.4 Proceso de levantamiento

**Paso 1 — Construir e iniciar todos los contenedores:**

```bash
docker-compose up --build -d
```

**Paso 2 — Verificar que todos los servicios estén activos:**

```bash
docker ps
```

**Paso 3 — Consultar logs de un servicio específico (opcional):**

```bash
docker logs eccl-api --follow
```

**Paso 4 — Detener el entorno:**

```bash
docker-compose down
```

---

## 4. Evidencias de Despliegue

A continuación se presentan las capturas de pantalla que evidencian el correcto funcionamiento del entorno desplegado.

### 4.1 Docker Desktop funcionando

> **📷 Insertar:** Captura de Docker Desktop activo mostrando el panel principal.

---

### 4.2 Contenedores activos

> **📷 Insertar:** Captura de la salida de `docker ps` o de la vista de contenedores en Docker Desktop.

Salida esperada de `docker ps`:

```
CONTAINER ID   IMAGE        COMMAND                  STATUS         PORTS                    NAMES
xxxxxxxxxxxx   eccl-api     "dotnet EcClientes..."   Up 2 minutes   0.0.0.0:8080->8080/tcp   eccl-api
xxxxxxxxxxxx   postgres:15  "docker-entrypoint..."   Up 2 minutes   5432/tcp                 eccl-db
```

---

### 4.3 Base de datos creada

> **📷 Insertar:** Captura de la base de datos creada con las tablas visibles (desde un cliente de BD o desde los logs del contenedor).

---

### 4.4 Endpoints funcionando

#### Swagger UI

> **📷 Insertar:** Captura de Swagger UI con los endpoints disponibles del módulo EcClientes.

#### Prueba con Postman

> **📷 Insertar:** Captura de una petición exitosa (GET, POST, PUT o DELETE) ejecutada desde Postman.

---

## 5. Referencia del CRUD

Las operaciones CRUD (Create, Read, Update, Delete) gestionan los recursos del módulo a través de los endpoints RESTful expuestos por la API.

### 5.1 Entidad: `Cliente`

| Método HTTP | Endpoint | Descripción |
|---|---|---|
| `GET` | `/api/clientes` | Obtiene la lista de todos los clientes registrados |
| `GET` | `/api/clientes/{id}` | Obtiene los datos de un cliente por su ID |
| `POST` | `/api/clientes` | Crea un nuevo cliente en el sistema |
| `PUT` | `/api/clientes/{id}` | Actualiza los datos de un cliente existente |
| `DELETE` | `/api/clientes/{id}` | Elimina un cliente por su ID |

#### Modelo `Cliente`

```json
{
  "id": 1,
  "nombre": "string",
  "apellido": "string",
  "correo": "string",
  "telefono": "string",
  "estado": true
}
```

> **📝 Completar:** Ajuste los campos del modelo según la entidad real de su proyecto.

---

### 5.2 Entidad: `DireccionCliente`

| Método HTTP | Endpoint | Descripción |
|---|---|---|
| `GET` | `/api/direcciones` | Lista todas las direcciones registradas |
| `GET` | `/api/direcciones/{id}` | Obtiene una dirección por su ID |
| `POST` | `/api/direcciones` | Crea una nueva dirección asociada a un cliente |
| `PUT` | `/api/direcciones/{id}` | Actualiza una dirección existente |
| `DELETE` | `/api/direcciones/{id}` | Elimina una dirección por su ID |

#### Modelo `DireccionCliente`

```json
{
  "id": 1,
  "clienteId": 1,
  "calle": "string",
  "ciudad": "string",
  "provincia": "string",
  "codigoPostal": "string",
  "esPrincipal": true
}
```

> **📝 Completar:** Ajuste los campos del modelo según la entidad real de su proyecto.

---

## 6. Conclusiones

> **📝 Completar:** Reemplace cada punto con sus reflexiones reales al concluir el módulo.

- **[C1]** _(Docker y entornos distribuidos)_ — Describa lo aprendido sobre contenedores Docker y su utilidad en arquitecturas de microservicios.
- **[C2]** _(Arquitectura del módulo)_ — Reflexione sobre las decisiones arquitectónicas tomadas y su impacto en la escalabilidad del sistema.
- **[C3]** _(Implementación del CRUD)_ — Evalúe la implementación de los endpoints RESTful y su conformidad con estándares REST.
- **[C4]** _(Desafíos y soluciones)_ — Describa los obstáculos encontrados durante el despliegue y cómo fueron resueltos.
- **[C5]** _(Valor académico-profesional)_ — Exponga el valor de esta práctica para su formación como desarrollador de software.

---

## 7. Referencias

- Docker Inc. (2024). *Docker Documentation*. https://docs.docker.com
- Kong Inc. (2024). *Kong Gateway Documentation*. https://docs.konghq.com
- > **📝 Completar:** Agregue las referencias bibliográficas utilizadas en formato APA o IEEE.

---

<sub>Instituto Superior Universitario Japón · Aplicaciones Distribuidas · 2026</sub>
