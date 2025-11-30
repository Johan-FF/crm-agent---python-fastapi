# Guía Rápida - PostgreSQL + FastAPI + Docker

## 🚀 Inicio Rápido

### 1. Preparar el entorno

```bash
# Clonar o entrar al directorio del proyecto
cd verticcal-crm-agent

# Copiar archivo de configuración (si es primera vez)
cp .env.example .env

# (Opcional) Agregar PIPEDRIVE_API_KEY en .env
```

### 2. Iniciar servicios con Docker Compose

```bash
# Iniciar todos los servicios
docker-compose up

# O en background
docker-compose up -d

# Ver logs en tiempo real
docker-compose logs -f
```

**Esperado en logs:**
```
db        | ... database system is ready to accept connections
db        | ... receiving stop signal
fastapi   | INFO: Uvicorn running on http://0.0.0.0:8000
fastapi   | ✓ Base de datos inicializada correctamente
n8n       | Ready to start workflows
```

### 3. Probar la API

```bash
# Health check
curl http://localhost:8000/contact/health

# Respuesta:
# {
#   "status": "healthy",
#   "timestamp": "2024-01-15T10:30:00",
#   "crm_configured": true/false
# }
```

## 📊 Base de Datos

### Acceder a PostgreSQL

```bash
# Conectar con psql
docker-compose exec db psql -U crm_user -d verticcal_crm

# Ver tablas
\dt

# Salir
\q
```

### Consultas SQL útiles

```sql
-- Ver estructura de tabla contacts
\d contacts

-- Listar todos los contactos
SELECT id, name, email, phone, crm_id FROM contacts;

-- Buscar por email
SELECT * FROM contacts WHERE email = 'john@example.com';

-- Contar contactos
SELECT COUNT(*) FROM contacts;

-- Ver timestamps
SELECT id, name, created_at, updated_at FROM contacts;
```

## 🧪 Probar Endpoints

### Crear Contacto

```bash
curl -X POST http://localhost:8000/contact \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "555-1234"
  }'

# Respuesta esperada:
# {
#   "success": true,
#   "message": "Contacto 'John Doe' creado exitosamente",
#   "contact_id": 1,
#   "crm_id": 12345,
#   "url": "https://app.pipedrive.com/person/12345",
#   "correlation_id": "abc-def-ghi"
# }
```

### Agregar Nota

```bash
curl -X POST http://localhost:8000/contact/note \
  -H "Content-Type: application/json" \
  -d '{
    "contact_id": 1,
    "content": "Cliente importante, seguimiento próxima semana"
  }'
```

### Actualizar Contacto

```bash
curl -X PATCH http://localhost:8000/contact \
  -H "Content-Type: application/json" \
  -d '{
    "contact_id": 1,
    "fields": {
      "phone": "555-9999"
    }
  }'
```

## 📚 API Documentation

```
# Swagger UI (interactive)
http://localhost:8000/docs

# ReDoc (read-only)
http://localhost:8000/redoc

# OpenAPI JSON
http://localhost:8000/openapi.json
```

## 🔧 Troubleshooting

### "Cannot connect to database"

```bash
# Verificar que PostgreSQL está corriendo
docker-compose ps

# Ver logs de BD
docker-compose logs db

# Reiniciar servicios
docker-compose restart db fastapi
```

### "Permission denied" en volúmenes

```bash
# Fix permisos en Mac/Linux
sudo chown -R $USER:$USER .

# O permitir a Docker
# En Windows/Mac: Docker Desktop settings → Resources → File Sharing
```

### "Port 5432 already in use"

```bash
# Matar proceso en puerto 5432
lsof -i :5432 | grep LISTEN | awk '{print $2}' | xargs kill -9

# O cambiar puerto en docker-compose.yml
# ports:
#   - "5433:5432"  # localhost:5433 -> container:5432
```

### Limpiar todo (⚠️ pierde datos)

```bash
# Detener y eliminar todo
docker-compose down -v

# Reiniciar desde cero
docker-compose up
```

## 📈 Performance Tips

### Desarrollo
- `NullPool` (actual) - Bueno para desarrollo
- Sin connection pooling - Cada request crea conexión nueva

### Producción (futura)
```python
# En config.py cambiar a:
poolclass=QueuePool  # Reutiliza conexiones
echo=False           # Desactiva logging SQL
```

## 🔐 Seguridad

### Cambiar credenciales (importante antes de producción)

1. Editar `.env`:
```env
DB_USER=mi_usuario
DB_PASSWORD=mi_contraseña_segura
DB_NAME=crm_produccion
```

2. Eliminar volumen anterior (pierde datos):
```bash
docker-compose down -v
docker-compose up  # Crea con nuevas credenciales
```

## 📝 Archivos Importantes

| Archivo | Propósito |
|---------|-----------|
| `docker-compose.yml` | Orquestación de servicios |
| `backend/requirements.txt` | Dependencias Python |
| `backend/app/db/base.py` | Configuración SQLAlchemy |
| `backend/app/models/contact.py` | Modelo ORM |
| `backend/app/repositories/contact_repository.py` | Acceso a datos |
| `backend/app/services/contact_service.py` | Lógica de negocio |
| `backend/app/api/v1/endpoints/contact.py` | Rutas API |
| `backend/app/main.py` | Aplicación FastAPI |
| `.env.example` | Plantilla de configuración |
| `docs/POSTGRESQL_INTEGRATION.md` | Documentación técnica |

## 🔄 Workflow Típico de Desarrollo

```bash
# 1. Clonar / entrar al proyecto
cd verticcal-crm-agent

# 2. Iniciar servicios
docker-compose up -d

# 3. Editar código (hot-reload habilitado)
# El código se recarga automáticamente

# 4. Probar cambios
curl http://localhost:8000/contact/health

# 5. Ver logs
docker-compose logs -f fastapi

# 6. Detener cuando termines
docker-compose down

# 7. O si hiciste cambios grandes
docker-compose down -v
docker-compose up
```

## 🎯 Próximas Mejoras

- [ ] Crear endpoints GET para recuperar contactos
- [ ] Implementar paginación avanzada
- [ ] Agregar filtros de búsqueda
- [ ] Crear migrations con Alembic
- [ ] Agregar autenticación JWT
- [ ] Implementar rate limiting
- [ ] Agregar tests unitarios

## 📞 Soporte

Para más información, ver:
- `docs/POSTGRESQL_INTEGRATION.md` - Documentación técnica completa
- `docs/REFACTORING_COMPLETE.md` - Arquitectura general
- `docs/QUICK_REFERENCE.md` - Referencia rápida de code
