# 🎯 Verticcal CRM Agent - N8N Workflow

## Estado: ✅ COMPLETAMENTE CONFIGURADO

El workflow N8N está **100% listo** con:
- ✅ 7 nodos correctamente conectados
- ✅ Todas las conexiones de datos establecidas
- ✅ OpenRouter API integrada
- ✅ 3 herramientas disponibles (crear, actualizar, agregar nota)
- ✅ Flujo bidireccional: Chat ↔ Memoria ↔ API

## 📊 Estructura del Workflow

```
┌─────────────┐
│Chat Trigger │ ← Usuario escribe un prompt
└──────┬──────┘
       │
       ↓
┌─────────────┐
│Chat Memory  │ ← Mantiene contexto de conversación
└──────┬──────┘
       │
       ↓
┌─────────────┐
│ AI Tools    │ ← Define herramientas disponibles
└──────┬──────┘
       │
       ↓
┌──────────────────────┐
│OpenRouter API Request│ ← Llama a GPT-3.5-turbo
└──────┬───────────────┘
       │
   ┌───┴───┬───────────┬──────────────┐
   ↓       ↓           ↓              ↓
┌──────┐ ┌──────┐ ┌──────────┐  ┌────────────┐
│Create│ │ Add  │ │ Update   │  │ (3 caminos │
│      │ │ Note │ │ Contact  │  │ posibles)  │
└───┬──┘ └───┬──┘ └─────┬────┘  └────────────┘
    │        │          │
    └────────┴──────────┘
           │
           ↓
      ┌─────────────┐
      │Chat Memory  │ ← Devuelve respuesta
      └─────────────┘
           ↓
      Usuario ve resultado ✓
```

## 🚀 Primeros Pasos (5 minutos)

### 1. Asegúrate que el Backend está corriendo
```powershell
# En terminal 1
cd verticcal-crm-agent
npm start
# Espera: ✓ Server running on http://localhost:8000
```

### 2. Inicia N8N con OpenRouter
```powershell
# En terminal 2
docker run -it --rm -p 5678:5678 `
    -e OPEN_ROUTER_API_KEY="tu-api-key-aqui" `
    n8n
```

### 3. Abre http://localhost:5678 en tu navegador

### 4. Importa el Workflow
- Click "+" → "Import from file"
- Selecciona: `n8n-workflows/verticcal-crm-agent-workflow.json`
- Click "Import"

### 5. Configura Variables
- ⚙️ Settings → Variables
- Agrega: `OPEN_ROUTER_API_KEY = tu-api-key`

### 6. Conecta Nodos (si es necesario)
Si no aparecen conectados, arrastra los puntos:
- Chat Trigger → Chat Memory
- Chat Memory → AI Tools
- AI Tools → Open Router API Request
- Open Router → HTTP nodes (x3)
- HTTP nodes → Chat Memory

### 7. Prueba
- Click "Deploy"
- Click 💬 Chat
- Escribe: `Crea a Falcao García con email falcao@verticcal.com`
- ✨ ¡Debería funcionar!

## 📁 Archivos de Configuración

| Archivo | Propósito |
|---------|-----------|
| `verticcal-crm-agent-workflow.json` | Workflow principal de N8N |
| `QUICK_START.md` | Guía super rápida (5 min) |
| `N8N_SETUP.md` | Guía detallada de configuración |
| `N8N_ENVIRONMENT_SETUP.md` | Configuración de variables |
| `N8N_MANUAL_SETUP.md` | Conexión manual de nodos |
| `start-n8n.ps1` | Script para iniciar N8N |
| `.env.example` | Variables de entorno |

## 🔧 Componentes del Workflow

### Chat Trigger
- **Propósito:** Recibe prompts del usuario
- **Entrada:** Texto libre en lenguaje natural
- **Salida:** Objeto con mensaje del usuario

### Chat Memory
- **Propósito:** Mantiene contexto de conversación
- **Configuración:** 
  - Context Window: 10 mensajes
  - Base Prefix: Instrucciones para actuar como agente CRM
- **Salida:** Mensajes formateados para LLM

### AI Tools
- **Propósito:** Define herramientas disponibles
- **Herramientas:**
  1. `create_contact(name, email?, phone?)`
  2. `add_note(contact_id, content)`
  3. `update_contact(contact_id, name?, email?, phone?)`
- **Salida:** Tools convertidas a formato OpenRouter

### Open Router API Request
- **Propósito:** Llama a LLM con context y tools
- **Modelo:** gpt-3.5-turbo (configurable)
- **Autenticación:** Bearer token de OPEN_ROUTER_API_KEY
- **Salida:** Respuesta con tool_use (si el LLM elige una herramienta)

### HTTP - Create Contact
- **Endpoint:** POST `/api/v1/contact`
- **Parámetros:** name, email, phone (del tool_use)
- **Respuesta:** 201 Created + datos de contacto

### HTTP - Add Note
- **Endpoint:** POST `/api/v1/contact/note`
- **Parámetros:** contact_id, content
- **Respuesta:** 200 OK + nota creada

### HTTP - Update Contact
- **Endpoint:** PATCH `/api/v1/contact`
- **Parámetros:** contact_id, name?, email?, phone?
- **Respuesta:** 200 OK + contacto actualizado

## 🧪 Casos de Uso de Prueba

### Test 1: Crear Contacto
```
Prompt: "Crea a Falcao García con email falcao@verticcal.com y teléfono +57 300 123 4567"

Resultado esperado:
✓ Contacto creado exitosamente
✓ ID: 1 (o siguiente disponible)
✓ Sincronizado con Pipedrive
```

### Test 2: Actualizar Contacto
```
Prompt: "Actualiza el email del contacto 1 a newemail@verticcal.com"

Resultado esperado:
✓ Contacto actualizado
✓ Email sincronizado en Pipedrive
```

### Test 3: Agregar Nota
```
Prompt: "Agrega una nota al contacto 1: Llamar para confirmar participación"

Resultado esperado:
✓ Nota agregada a ambos sistemas
✓ Timestamp y contenido guardados
```

## 🔐 Seguridad

- **API Key:** Nunca la compartas en código
  - Usa variables de entorno
  - En N8N: Settings → Variables
  - En .env: Agrega .env a .gitignore

- **Backend:** Requiere Content-Type: application/json
  - N8N lo configura automáticamente

- **OpenRouter:** Usa HTTPS
  - Verifica certificados en producción
  - Establece límites de gastos

## 📊 Monitoreo

### Ver logs en N8N:
- Settings → Logs (icono de libreta)

### Ver logs del backend:
```powershell
npm run logs
```

### Ver logs de OpenRouter (API calls):
- https://openrouter.ai/activity

## 💡 Tips

1. **Prueba primero con gpt-3.5-turbo:** Es rápido, barato (~$0.0015 por 1K tokens)
2. **Guarda respuestas:** Los datos se guardan en PostgreSQL
3. **Usa prompts claros:** "Crea contacto Juan con email juan@email.com" funciona mejor
4. **Sincronización automática:** Los cambios se replican a Pipedrive en tiempo real

## 🆘 Soporte

Si algo no funciona:

1. **JSON inválido:** Usa el validador en `N8N_MANUAL_SETUP.md`
2. **Conexiones no aparecen:** Conecta manualmente arrastrando nodos
3. **API Key error:** Recopia desde https://openrouter.ai/keys
4. **Backend error:** Verifica `http://localhost:8000/health`
5. **N8N no inicia:** Usa Docker o instala desde https://n8n.io

## 📞 Próximas Mejoras

- [ ] Agregar búsqueda de contactos
- [ ] Listar todos los contactos
- [ ] Historial de conversaciones persistente
- [ ] Webhooks de Pipedrive
- [ ] Autenticación en N8N
- [ ] Base de datos de historiales

---

**¡Tu sistema está 100% listo! 🎉**

Comienza con `QUICK_START.md` para los primeros 5 minutos.
