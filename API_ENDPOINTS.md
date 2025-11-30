# 📋 API Endpoints - Verticcal CRM

Base URL: `http://localhost:8000/api/v1`

---

## 1️⃣ Health Check

**Endpoint:** `GET /contact/health`

**Descripción:** Verifica el estado de la API y configuración del CRM

### Linux/Mac (curl)
```bash
curl -X GET "http://localhost:8000/api/v1/contact/health" \
  -H "Content-Type: application/json"
```

### Windows (PowerShell)
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/api/v1/contact/health" -Method GET -Headers @{"Content-Type"="application/json"}
```

**Respuesta esperada (200 OK):**
```json
{
  "status": "healthy",
  "crm_configured": true,
  "mock_mode": false,
  "timestamp": "2025-11-30T18:55:36"
}
```

---

## 2️⃣ Crear Contacto

**Endpoint:** `POST /contact`

**Descripción:** Crea un nuevo contacto (intenta primero en Pipedrive, fallback a PostgreSQL)

### Linux/Mac (curl)
```bash
curl -X POST "http://localhost:8000/api/v1/contact" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Juan Pérez",
    "email": "juan.perez@example.com",
    "phone": "+34612345678"
  }'
```

### Windows (PowerShell)
```powershell
$body = @{
    name = "Juan Pérez"
    email = "juan.perez@example.com"
    phone = "+34612345678"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/api/v1/contact" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

**Parámetros:**
- `name` (string, requerido): Nombre del contacto
- `email` (string, opcional): Email del contacto
- `phone` (string, opcional): Teléfono del contacto

**Respuesta esperada (200 OK):**
```json
{
  "success": true,
  "message": "Contacto creado en Pipedrive",
  "contact_id": 1,
  "crm_id": 42,
  "name": "Juan Pérez",
  "email": "juan.perez@example.com",
  "phone": "+34612345678",
  "correlation_id": "abc123-def456"
}
```

**Respuesta si falla Pipedrive (Fallback a PostgreSQL):**
```json
{
  "success": true,
  "message": "Contacto creado en PostgreSQL (BD local)",
  "contact_id": 2,
  "crm_id": null,
  "name": "María García",
  "email": "maria@example.com",
  "phone": "+34698765432",
  "correlation_id": "xyz789-uvw012"
}
```

---

## 3️⃣ Actualizar Contacto

**Endpoint:** `PATCH /contact`

**Descripción:** Actualiza un contacto existente (intenta primero en Pipedrive, fallback a PostgreSQL)

### Opción A: Actualizar por campos individuales

**Linux/Mac (curl):**
```bash
curl -X PATCH "http://localhost:8000/api/v1/contact" \
  -H "Content-Type: application/json" \
  -d '{
    "contact_id": 1,
    "phone": "+34611111111"
  }'
```

**Windows (PowerShell):**
```powershell
$body = @{
    contact_id = 1
    phone = "+34611111111"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/api/v1/contact" `
    -Method PATCH `
    -Body $body `
    -ContentType "application/json"
```

### Opción B: Actualizar múltiples campos

**Linux/Mac (curl):**
```bash
curl -X PATCH "http://localhost:8000/api/v1/contact" \
  -H "Content-Type: application/json" \
  -d '{
    "contact_id": 1,
    "name": "Juan Pérez Updated",
    "email": "juan.updated@example.com",
    "phone": "+34699999999"
  }'
```

**Windows (PowerShell):**
```powershell
$body = @{
    contact_id = 1
    name = "Juan Pérez Updated"
    email = "juan.updated@example.com"
    phone = "+34699999999"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/api/v1/contact" `
    -Method PATCH `
    -Body $body `
    -ContentType "application/json"
```

### Opción C: Usar objeto fields

**Linux/Mac (curl):**
```bash
curl -X PATCH "http://localhost:8000/api/v1/contact" \
  -H "Content-Type: application/json" \
  -d '{
    "contact_id": 1,
    "fields": {
      "phone": "+34611111111",
      "status": "Qualified"
    }
  }'
```

**Windows (PowerShell):**
```powershell
$body = @{
    contact_id = 1
    fields = @{
        phone = "+34611111111"
        status = "Qualified"
    }
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/api/v1/contact" `
    -Method PATCH `
    -Body $body `
    -ContentType "application/json"
```

**Parámetros:**
- `contact_id` (integer, requerido): ID del contacto a actualizar
- `name` (string, opcional): Nuevo nombre
- `email` (string, opcional): Nuevo email
- `phone` (string, opcional): Nuevo teléfono
- `fields` (object, opcional): Otros campos adicionales

**Respuesta esperada (200 OK):**
```json
{
  "success": true,
  "message": "Contacto actualizado en Pipedrive",
  "contact_id": 1,
  "phone": "+34611111111",
  "correlation_id": "pqr345-stu678"
}
```

---

## 4️⃣ Agregar Nota a Contacto

**Endpoint:** `POST /contact/note`

**Descripción:** Agrega una nota a un contacto existente (intenta primero en Pipedrive, fallback local)

### Linux/Mac (curl)
```bash
curl -X POST "http://localhost:8000/api/v1/contact/note" \
  -H "Content-Type: application/json" \
  -d '{
    "contact_id": 1,
    "content": "This is a test note from the API"
  }'
```

### Windows (PowerShell)
```powershell
$body = @{
    contact_id = 1
    content = "This is a test note from the API"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/api/v1/contact/note" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

**Parámetros:**
- `contact_id` (integer, requerido): ID del contacto
- `content` (string, requerido): Contenido de la nota

**Respuesta esperada (200 OK):**
```json
{
  "success": true,
  "message": "Nota agregada en Pipedrive",
  "contact_id": 1,
  "note_id": 15,
  "correlation_id": "jkl901-mno234"
}
```

---

## 🔄 Flujo CRM-First

Todos los endpoints (excepto Health) siguen este flujo:

```
1. Intenta crear/actualizar/agregar en Pipedrive
   ├─ ✅ SI FUNCIONA: Guarda también en PostgreSQL
   │    └─ Devuelve: crm_id + contact_id
   │
   └─ ❌ SI FALLA (401, timeout, etc): 
        └─ Fallback a PostgreSQL
        └─ Devuelve: contact_id (sin crm_id)
```

---

## 🧪 Ejemplos Completos de Prueba

### Prueba 1: Crear contacto

**Linux/Mac (bash):**
```bash
# Crear contacto
RESPONSE=$(curl -s -X POST "http://localhost:8000/api/v1/contact" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Sofia Martinez",
    "email": "sofia@example.com",
    "phone": "+34621234567"
  }')

echo $RESPONSE

# Guardar el contact_id para usar en otros requests
CONTACT_ID=$(echo $RESPONSE | grep -o '"contact_id":[0-9]*' | head -1 | grep -o '[0-9]*')
echo "Contact ID: $CONTACT_ID"
```

**Windows (PowerShell):**
```powershell
# Crear contacto
$body = @{
    name = "Sofia Martinez"
    email = "sofia@example.com"
    phone = "+34621234567"
} | ConvertTo-Json

$response = Invoke-WebRequest -Uri "http://localhost:8000/api/v1/contact" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"

$data = $response.Content | ConvertFrom-Json
Write-Host "Response: $($response.Content)"

# Guardar el contact_id para usar en otros requests
$CONTACT_ID = $data.contact_id
Write-Host "Contact ID: $CONTACT_ID"
```

### Prueba 2: Actualizar teléfono

**Linux/Mac (bash):**
```bash
# Actualizar teléfono (cambiar por el contact_id obtenido)
curl -X PATCH "http://localhost:8000/api/v1/contact" \
  -H "Content-Type: application/json" \
  -d '{
    "contact_id": 1,
    "phone": "+34699999999"
  }'
```

**Windows (PowerShell):**
```powershell
# Actualizar teléfono (cambiar por el contact_id obtenido)
$body = @{
    contact_id = 1
    phone = "+34699999999"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/api/v1/contact" `
    -Method PATCH `
    -Body $body `
    -ContentType "application/json"
```

### Prueba 3: Agregar nota

**Linux/Mac (bash):**
```bash
# Agregar nota (cambiar por el contact_id obtenido)
curl -X POST "http://localhost:8000/api/v1/contact/note" \
  -H "Content-Type: application/json" \
  -d '{
    "contact_id": 1,
    "content": "Primera nota de prueba"
  }'
```

**Windows (PowerShell):**
```powershell
# Agregar nota (cambiar por el contact_id obtenido)
$body = @{
    contact_id = 1
    content = "Primera nota de prueba"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/api/v1/contact/note" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

### Prueba 4: Agregar segunda nota

**Linux/Mac (bash):**
```bash
curl -X POST "http://localhost:8000/api/v1/contact/note" \
  -H "Content-Type: application/json" \
  -d '{
    "contact_id": 1,
    "content": "Segunda nota con más información"
  }'
```

**Windows (PowerShell):**
```powershell
$body = @{
    contact_id = 1
    content = "Segunda nota con más información"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/api/v1/contact/note" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

---

## 📊 Códigos de Respuesta

| Código | Descripción |
|--------|-------------|
| `200` | OK - Operación exitosa |
| `400` | Bad Request - Datos inválidos o incompletos |
| `422` | Unprocessable Entity - Validación de schema falló |
| `502` | Bad Gateway - Error procesando la solicitud |

---

## 🔍 Logs

Para ver los logs de la API en tiempo real:

```bash
docker compose logs -f fastapi
```

Buscar operaciones específicas:
```bash
# Ver todos los creates
docker compose logs fastapi | grep "Crear contacto"

# Ver todas las actualizaciones
docker compose logs fastapi | grep "Actualizar contacto"

# Ver todas las notas
docker compose logs fastapi | grep "Crear nota"

# Ver todos los errores
docker compose logs fastapi | grep "ERROR"

# Ver operaciones de Pipedrive
docker compose logs fastapi | grep "Pipedrive"

# Ver fallbacks a PostgreSQL
docker compose logs fastapi | grep "PostgreSQL"
```

---

## 🗄️ Base de Datos

Consultar contactos directamente en PostgreSQL:

```bash
# Conectar a la BD
docker compose exec db psql -U crm_user -d verticcal_crm

# Listar todos los contactos
SELECT id, name, email, phone, crm_id, created_at FROM contacts;

# Listar notas
SELECT id, contact_id, content, created_at FROM notes;

# Contar total de contactos
SELECT COUNT(*) FROM contacts;
```

---

## ⚙️ Configuración

**Archivo:** `docker-compose.yml`

Variables importantes:
- `PIPEDRIVE_API_KEY`: API key de Pipedrive
- `PIPEDRIVE_BASE_URL`: URL base de la API de Pipedrive (default: `https://api.pipedrive.com/v1`)
- `DATABASE_URL`: URL de conexión a PostgreSQL
- `LOG_LEVEL`: Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)

---

## 🐛 Troubleshooting

### Mostrar respuesta formateada (Windows)

Si quieres ver la respuesta JSON de forma legible en PowerShell:

```powershell
# Guardar respuesta y mostrar formateada
$response = Invoke-WebRequest -Uri "http://localhost:8000/api/v1/contact" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"

$response.Content | ConvertFrom-Json | ConvertTo-Json -Depth 5
```

### Error 401 en Pipedrive
Si ves errores 401, significa que el API key de Pipedrive:
- No tiene permisos de escritura
- Es inválido
- La cuenta está en modo demo/trial

**Solución:** Verificar el API key en https://app.pipedrive.com/settings/personal/api

### Error de conexión a BD
```bash
# Verificar que PostgreSQL está corriendo
docker compose ps

# Ver logs de PostgreSQL
docker compose logs db
```

### Hot reload no funciona
```bash
# Reiniciar los contenedores
docker compose restart fastapi
```

---

## 📝 Notas

- Todos los requests deben incluir `Content-Type: application/json`
- El API es **resiliente**: si falla Pipedrive, automáticamente guarda en PostgreSQL
- Cada operación genera un `correlation_id` único para rastrearla en los logs
- El teléfono debe incluir el código de país (ej: +34 para España)

