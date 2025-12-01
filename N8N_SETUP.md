# Setup del Workflow N8N - Verticcal CRM Agent

## Requisitos Previos

1. **N8N ejecutándose** en `http://localhost:5678`
2. **Backend corriendo** en `http://localhost:8000`
3. **PostgreSQL** corriendo (con Docker Compose o local)
4. **Cuenta en OpenRouter** con API key válida

## Pasos de Configuración

### 1. Importar el Workflow

- Abre N8N: `http://localhost:5678`
- Ve a "Workflows" → "New" → "Import from file"
- Selecciona: `n8n-workflows/verticcal-crm-agent-workflow.json`
- Haz clic en "Import"

### 2. Configurar Variables de Entorno

En N8N, ve a **Settings** → **Environment Variables** y agrega:

```
OPEN_ROUTER_API_KEY = tu_api_key_aqui
OPEN_ROUTER_MODEL = openai/gpt-3.5-turbo (opcional)
```

**Para obtener API Key de OpenRouter:**
1. Registrarse en https://openrouter.ai
2. Ir a https://openrouter.ai/keys
3. Crear una nueva API key
4. Copiar y pegar en N8N

### 3. Verificar Nodos Conectados

Después de importar, verifica que los nodos estén así conectados:

```
Chat Trigger 
    ↓
Chat Memory 
    ↓
AI Tools 
    ↓
Open Router API Request
    ↓ (se abre en 3 HTTP nodes paralelos)
HTTP - Create Contact
HTTP - Add Note
HTTP - Update Contact
```

Todos los HTTP nodes devuelven a Chat Memory para continuar la conversación.

### 4. Configuración de Cada Nodo

#### Chat Trigger
✅ Ya configurado - acepta prompts del usuario

#### Chat Memory
✅ Ya configurado con:
- Context Window: 10 mensajes
- Base Prefix: instrucciones para actuar como agente CRM
- Session ID: por URL

#### AI Tools
✅ Define 3 herramientas disponibles:
1. **create_contact** - Crea nuevo contacto (requiere: name)
2. **add_note** - Agrega nota (requiere: contact_id, content)
3. **update_contact** - Actualiza contacto (requiere: contact_id)

#### Open Router API Request
✅ Usa GPT-3.5-turbo (o modelo configurado)
- Envía messages y tools como JSON
- OpenRouter interpreta qué herramienta usar
- Devuelve tool_use con parámetros

#### HTTP Nodes
✅ Mapean herramientas a endpoints locales:
- POST `/api/v1/contact` → crear contacto
- POST `/api/v1/contact/note` → agregar nota
- PATCH `/api/v1/contact` → actualizar contacto

## Prueba del Flujo Completo

### Test 1: Crear Contacto

**Prompt:**
```
Crea a Falcao García con correo falcao@verticcal.com y teléfono +57 300 123 4567
```

**Flujo esperado:**
1. Chat Trigger recibe el prompt
2. Chat Memory lo almacena
3. AI Tools lo procesa y detecta: `create_contact(name="Falcao García", email="falcao@verticcal.com", phone="+57 300 123 4567")`
4. Open Router extrae los parámetros
5. HTTP - Create Contact hace POST a `/api/v1/contact`
6. Backend crea el contacto y devuelve `201 Created`
7. Chat Memory recibe respuesta: "Contacto Falcao García creado exitosamente"

**Respuesta esperada:**
```
Contacto Falcao García creado exitosamente con ID: 1
Email: falcao@verticcal.com
Teléfono: +57 300 123 4567
```

### Test 2: Agregar Nota

**Prompt:**
```
Agrega una nota al contacto 1: "Potencial cliente para sponsor de equipo"
```

**Flujo esperado:**
1. AI Tools detecta: `add_note(contact_id=1, content="...")`
2. HTTP - Add Note hace POST a `/api/v1/contact/note`
3. Backend agrega nota a Pipedrive
4. Respuesta: "Nota agregada al contacto"

### Test 3: Actualizar Contacto

**Prompt:**
```
Actualiza el teléfono del contacto 1 a +57 320 987 6543
```

**Flujo esperado:**
1. AI Tools detecta: `update_contact(contact_id=1, phone="+57 320 987 6543")`
2. HTTP - Update Contact hace PATCH a `/api/v1/contact`
3. Backend actualiza el contacto
4. Respuesta: "Contacto actualizado"

## Solución de Problemas

### Error: "Variable not found: OPEN_ROUTER_API_KEY"
**Solución:** Configurar la variable de entorno en N8N Settings

### Error: "Connection refused" en HTTP nodes
**Solución:** Verificar que el backend está corriendo en `http://localhost:8000`

### Error: "401 Unauthorized" en Open Router
**Solución:** Verificar que la API key sea válida

### El workflow no avanza del nodo "AI Tools"
**Solución:** 
- Verificar que Open Router API key esté configurada
- Revisar logs de N8N (Settings → Logs)
- Probar llamada manual a Open Router con curl:
```bash
curl -X POST https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "HTTP-Referer: https://verticcal-crm-agent.local" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "openai/gpt-3.5-turbo",
    "messages": [{"role": "user", "content": "Hola"}],
    "tools": [],
    "tool_choice": "auto"
  }'
```

### Los datos no llegan a la API local
**Solución:**
- Verificar que las expresiones `$json.tool_use.input.*` están correctas
- Abrir DevTools de N8N (F12) para ver logs detallados
- Revisar en el nodo HTTP los valores que se envían

## URLs de Referencia

- **N8N Dashboard:** `http://localhost:5678`
- **Backend API:** `http://localhost:8000`
- **Documentación API:** `http://localhost:8000/docs` (Swagger)
- **OpenRouter:** `https://openrouter.ai`

## Próximas Mejoras

1. Agregar autenticación a N8N
2. Configurar base de datos para almacenar historiales
3. Agregar más herramientas (buscar contactos, listar, etc.)
4. Integración con webhook de Pipedrive
5. Soporte para múltiples idiomas

