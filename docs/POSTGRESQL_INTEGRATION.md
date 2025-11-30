# Integración PostgreSQL - Guía Completa

## 📋 Resumen Ejecutivo

Se ha integrado **PostgreSQL** como base de datos persistente para la aplicación. La base de datos se crea automáticamente cuando se inicia la aplicación mediante Docker Compose.

**Estado:** ✅ 100% Completado

## 🏗️ Arquitectura

### Diagrama de Capas

```
┌─────────────────────────────────────────┐
│       FastAPI Endpoints (Router)        │ ← Recibe solicitudes HTTP
└──────────────┬──────────────────────────┘
               │ Depends(get_db)
               ↓
┌─────────────────────────────────────────┐
│       Servicios (ContactService)        │ ← Lógica de negocio
└──────────────┬──────────────────────────┘
               │
               ↓
┌─────────────────────────────────────────┐
│  Repositorios (ContactRepository)       │ ← Acceso a datos
│  - Métodos BD Local (PostgreSQL)        │
│  - Métodos CRM (Pipedrive API)          │
└──────────────┬──────────────────────────┘
               │
        ┌──────┴──────┐
        ↓             ↓
   PostgreSQL    Pipedrive API
    (Local)       (External)
```

### Flujo de Datos

```
Cliente HTTP
    │
    ├→ POST /contact
    │   └→ ContactService.create_contact()
    │       ├→ ContactRepository.create_local()      [PostgreSQL]
    │       │   └→ INSERT INTO contacts
    │       │
    │       └→ ContactRepository.create_in_crm()    [Pipedrive API]
    │           └→ POST /persons (si hay API key)
    │
    └→ Response (ContactResponse)
```

## 🔧 Componentes Técnicos

### 1. Base de Datos (PostgreSQL)

**Ubicación:** `backend/app/db/base.py`

```python
# Motor SQLAlchemy
engine = create_engine(
    settings.DATABASE_URL,
    echo=False,
    poolclass=NullPool  # Desarrollo: sin pool
)

# Factory de sesiones
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base ORM
Base = declarative_base()

# Inicialización
def init_db():
    Base.metadata.create_all(bind=engine)  # Crea tablas

def close_db():
    engine.dispose()  # Cierra conexiones
```

**Características:**
- ✅ Auto-inicialización en startup
- ✅ Creación automática de tablas
- ✅ Persistencia de datos (volumen Docker)
- ✅ Transactions automáticas
- ✅ Connection pooling (configurable)

### 2. Modelo ORM - Contact

**Ubicación:** `backend/app/models/contact.py`

```python
class Contact(Base):
    __tablename__ = "contacts"
    
    id: int              # PK, autoincrement
    name: str            # Required, indexed
    email: str           # Unique, indexed
    phone: str           # Optional
    crm_id: int          # Pipedrive ID, unique
    created_at: datetime # Server default
    updated_at: datetime # Server default + onupdate
```

**Índices:**
- `id` (primary key)
- `name` (búsqueda frecuente)
- `email` (búsqueda y validación de duplicados)
- `crm_id` (sincronización Pipedrive)

### 3. Inyección de Dependencias

**Ubicación:** `backend/app/db/session.py`

```python
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Uso en endpoints:
@router.post("")
async def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    service = ContactService(db)
    return service.create_contact(contact)
```

### 4. Repositorio - Métodos Locales

**Ubicación:** `backend/app/repositories/contact_repository.py`

#### Escritura
- `create_local()` - INSERT nuevo contacto
- `update()` - UPDATE contacto existente
- `delete()` - DELETE contacto

#### Lectura
- `get_by_id()` - Query por ID
- `get_by_email()` - Query por email (unique)
- `get_by_crm_id()` - Query por ID Pipedrive
- `get_by_name()` - ILIKE search
- `get_all()` - Listado con paginación

### 5. Sincronización Dual

El repositorio mantiene sincronización con Pipedrive:

```python
def create_local(self, name, email, phone, crm_id):
    # Guarda en PostgreSQL
    contact = Contact(...)
    self.db.add(contact)
    self.db.commit()
    return contact

def create_in_crm(self, name, email, phone):
    # Sincroniza con Pipedrive API
    # (Si PIPEDRIVE_API_KEY está configurada)
    response = requests.post(...)
    return response.json()
```

## 🐳 Docker Compose

**Ubicación:** `docker-compose.yml`

```yaml
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: crm_user
      POSTGRES_PASSWORD: crm_password
      POSTGRES_DB: verticcal_crm
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U crm_user"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - crm-network

  api:
    depends_on:
      db:
        condition: service_healthy  # Espera health check
    environment:
      DATABASE_URL: postgresql://crm_user:crm_password@db:5432/verticcal_crm
    networks:
      - crm-network

volumes:
  postgres_data:  # Persistencia entre restarts
```

**Características:**
- ✅ Health checks automáticos
- ✅ API espera a que BD esté lista
- ✅ Persistencia de datos (volumen)
- ✅ Red interna (crm-network)
- ✅ PostgreSQL 16-alpine (lightweight)

## 📦 Dependencias

**Nuevas en `requirements.txt`:**

```
sqlalchemy==2.0.23        # ORM para Python
psycopg2-binary==2.9.9    # Adaptador PostgreSQL
alembic==1.13.0           # Migrations (futuro)
```

## 🚀 Flujo de Inicio

1. **Docker Compose inicia:**
   ```bash
   docker-compose up
   ```

2. **PostgreSQL se inicia:**
   - Contenedor: `verticcal-crm-postgres`
   - Health check: `pg_isready -U crm_user`
   - Estado: HEALTHY (ready)

3. **FastAPI espera health check:**
   ```yaml
   depends_on:
     db:
       condition: service_healthy
   ```

4. **FastAPI inicia y ejecuta lifespan startup:**
   ```python
   # En main.py
   @asynccontextmanager
   async def lifespan(app: FastAPI):
       logger.info("Inicializando BD...")
       init_db()  # ← AQUÍ se crean las tablas
       yield
       close_db()
   ```

5. **Tablas se crean automáticamente:**
   - `Base.metadata.create_all(bind=engine)`
   - Se ejecuta solo si no existen

6. **API está lista:**
   - Endpoint `/contact` funcional
   - BD sincronizada con ORM
   - Listo para peticiones HTTP

## 📝 Operaciones CRUD

### CREATE
```python
# POST /contact
contact_data = ContactCreate(name="John", email="john@example.com")
service = ContactService(db)
response = service.create_contact(contact_data)

# Resultado:
# - INSERT en tabla contacts
# - POST a Pipedrive API (si está configurada)
# - crm_id guardado en BD
```

### READ
```python
# GET implícitos (en futuro)
contact = repository.get_by_id(1)
contact = repository.get_by_email("john@example.com")
contacts = repository.get_all(skip=0, limit=10)
```

### UPDATE
```python
# PATCH /contact
update_data = ContactUpdate(contact_id=1, fields={"phone": "555-1234"})
service = ContactService(db)
response = service.update_contact(update_data)

# Resultado:
# - UPDATE en tabla contacts
# - PUT a Pipedrive API (si está configurada)
```

### DELETE
```python
# DELETE implícito (en futuro)
success = repository.delete(1)

# Resultado:
# - DELETE en tabla contacts
```

## 🔐 Manejo de Transacciones

```python
try:
    contact = Contact(name="John", email="john@example.com")
    db.add(contact)
    db.commit()         # ✅ Auto-commit
    db.refresh(contact) # Actualiza objeto con datos BD
    return contact
except IntegrityError as e:
    db.rollback()       # ❌ Rollback en error
    logger.error(f"Violación de constraint: {e}")
    raise
```

## 🔄 Manejo de Errores

### Duplicado de Email
```
IntegrityError → Rollback
HTTP 409 Conflict
"Ya existe un contacto con email..."
```

### Conexión BD fallida
```
DatabaseError → Rollback
HTTP 502 Bad Gateway
"Error comunicándose con la BD"
```

### API Pipedrive no disponible
```
RequestException → WARNING log
Contacto se guarda en BD local
crm_id = None (sin sincronización)
```

## 📊 Variables de Entorno

| Variable | Valor | Descripción |
|----------|-------|-------------|
| `DB_USER` | crm_user | Usuario PostgreSQL |
| `DB_PASSWORD` | crm_password | Contraseña BD |
| `DB_NAME` | verticcal_crm | Nombre BD |
| `DB_HOST` | db | Host (nombre servicio Docker) |
| `DB_PORT` | 5432 | Puerto PostgreSQL |
| `DATABASE_URL` | postgresql://... | URL completa |
| `PIPEDRIVE_API_KEY` | (vacío) | Key para sincronización |

## 🔍 Verificación

### Logs de startup exitoso
```
✓ Base de datos inicializada correctamente
✓ Conexiones de base de datos cerradas
```

### Verificar tablas creadas
```bash
docker-compose exec db psql -U crm_user -d verticcal_crm -c "\dt"
```

Resultado esperado:
```
         List of relations
 Schema | Name     | Type  | Owner
--------+----------+-------+----------
 public | contacts | table | crm_user
```

### Probar conexión
```bash
docker-compose exec db psql -U crm_user -d verticcal_crm -c "SELECT * FROM contacts;"
```

## 🚦 Comandos Docker Útiles

```bash
# Iniciar servicios
docker-compose up

# Detener servicios
docker-compose down

# Detener y eliminar volúmenes (CUIDADO: pierde datos)
docker-compose down -v

# Ver logs
docker-compose logs -f api    # FastAPI
docker-compose logs -f db     # PostgreSQL

# Acceder a BD
docker-compose exec db psql -U crm_user -d verticcal_crm

# Reiniciar servicio
docker-compose restart api
```

## 📈 Próximos Pasos (Opcionales)

### 1. Alembic Migrations
```bash
# Crear estructura Alembic (no implementada aún)
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### 2. Production Setup
```python
# En config.py cambiar para producción:
poolclass=QueuePool  # en lugar de NullPool
echo=False           # ya está
```

### 3. Backups
```bash
# Backup BD
docker-compose exec db pg_dump -U crm_user verticcal_crm > backup.sql

# Restore
docker-compose exec -T db psql -U crm_user verticcal_crm < backup.sql
```

## 📚 Referencias

- [SQLAlchemy ORM](https://docs.sqlalchemy.org/en/20/)
- [FastAPI Dependency Injection](https://fastapi.tiangolo.com/tutorial/dependencies/)
- [PostgreSQL Docker](https://hub.docker.com/_/postgres)
- [Docker Compose Health Checks](https://docs.docker.com/compose/compose-file/05-services/#healthcheck)

## ✅ Checklist de Integración

- ✅ PostgreSQL en docker-compose.yml
- ✅ SQLAlchemy engine configurado
- ✅ Modelo Contact como ORM
- ✅ SessionLocal factory creada
- ✅ get_db() dependency injection
- ✅ ContactRepository con métodos BD
- ✅ ContactService recibe db parameter
- ✅ Endpoints inyectan db dependency
- ✅ init_db() en lifespan startup
- ✅ .env.example actualizado
- ✅ Documentación completa

---

**Última actualización:** 2024
**Versión:** 1.0
