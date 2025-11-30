# API Routes - Migration Guide

## Route Changes Summary

The backend has been refactored with new API routes. Update any n8n workflows or external integrations accordingly.

### Endpoint Mapping

| Purpose | OLD Route | NEW Route | Method |
|---------|-----------|-----------|--------|
| Create Contact | `/crm/contact` | `/api/v1/contact` | POST |
| Add Note | `/crm/contact/note` | `/api/v1/contact/note` | POST |
| Update Contact | `/crm/contact` | `/api/v1/contact` | PATCH |
| Health Check | `/health` | `/api/v1/contact/health` | GET |
| API Root | N/A | `/` | GET |

---

## Request/Response Examples

### 1. Create Contact
```bash
curl -X POST http://localhost:8000/api/v1/contact \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Juan Pérez",
    "email": "juan@example.com",
    "phone": "+57 300 123 4567"
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "Contacto 'Juan Pérez' creado exitosamente",
  "contact_id": 12345,
  "crm_id": 12345,
  "url": "https://app.pipedrive.com/person/12345",
  "correlation_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479"
}
```

### 2. Add Note
```bash
curl -X POST http://localhost:8000/api/v1/contact/note \
  -H "Content-Type: application/json" \
  -d '{
    "contact_id": 12345,
    "content": "Cliente interesado en plan Premium"
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "Nota agregada al contacto 12345",
  "contact_id": 12345,
  "url": "https://app.pipedrive.com/person/12345",
  "correlation_id": "abc123..."
}
```

### 3. Update Contact
```bash
curl -X PATCH http://localhost:8000/api/v1/contact \
  -H "Content-Type: application/json" \
  -d '{
    "contact_id": 12345,
    "fields": {
      "phone": "+57 311 999 0000",
      "status": "Qualified"
    }
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "Contacto 12345 actualizado",
  "contact_id": 12345,
  "url": "https://app.pipedrive.com/person/12345",
  "correlation_id": "xyz789..."
}
```

### 4. Health Check
```bash
curl http://localhost:8000/api/v1/contact/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:45.123456",
  "crm_configured": true
}
```

---

## Error Responses

### 400 - Bad Request
```json
{
  "detail": "El nombre debe tener al menos 2 caracteres"
}
```

### 409 - Conflict (Duplicate)
```json
{
  "detail": "Ya existe un contacto con email juan@example.com. ID: 9999"
}
```

### 502 - Bad Gateway (API Error)
```json
{
  "detail": "Error comunicándose con el CRM"
}
```

---

## Interactive Documentation

Once the server is running, access:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **OpenAPI JSON:** http://localhost:8000/openapi.json

These provide interactive request/response examples.

---

## Correlation ID Tracking

Every request gets a unique `correlation_id` (UUID) for tracking:

```
Response: "correlation_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479"

Check logs:
[2024-01-15 10:30:45] [f47ac10b-58cc-4372-a567-0e02b2c3d479] Crear contacto: Juan Pérez
[2024-01-15 10:30:45] [f47ac10b-58cc-4372-a567-0e02b2c3d479] Contacto creado: ID=12345
```

Use the correlation_id to trace request flow in logs.

---

## Configuration

Update your `.env` file:
```env
PIPEDRIVE_API_KEY=your_api_key_here
PIPEDRIVE_BASE_URL=https://api.pipedrive.com/v1
LOG_LEVEL=INFO
```

---

## Testing with n8n

In n8n HTTP Request nodes, update the URLs:

**Old:**
```
http://backend:8000/crm/contact
```

**New:**
```
http://backend:8000/api/v1/contact
```

The request body and response format remain the same.

---

## Backward Compatibility

The old `backend/main.py` file still works and imports from the new modular structure.
Both entry points are supported:

```bash
# Both work:
python -m uvicorn main:app --reload
python -m uvicorn app.main:app --reload
```

---

## Questions?

1. Check `/docs` for interactive API documentation
2. See `REFACTORING_COMPLETE.md` for architecture details
3. Review module docstrings in `app/` for component details
