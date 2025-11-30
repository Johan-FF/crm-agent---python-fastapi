# Guía de Setup con Open Router

## ¿Qué es Open Router?

**Open Router** es una plataforma que proporciona acceso unificado a múltiples modelos LLM (ChatGPT, Claude, Llama, etc.) con una sola API.

**Ventajas sobre OpenAI directo:**
- ✅ Acceso a múltiples modelos (GPT-4, Claude 3, Llama 2, etc.)
- ✅ Precios más competitivos
- ✅ Soporte fallback automático si un modelo no está disponible
- ✅ Dashboard con analytics de uso
- ✅ Control granular del gasto

---

## Paso 1: Registrarse en Open Router

1. Ve a **[https://openrouter.ai](https://openrouter.ai)**
2. Haz clic en **"Sign up"** (esquina superior derecha)
3. Crea tu cuenta (email + contraseña)
4. Confirma tu email

---

## Paso 2: Obtener tu API Key

1. Una vez logueado, ve a **[https://openrouter.ai/keys](https://openrouter.ai/keys)**
2. Haz clic en **"Create new"** (o "Create API Key")
3. Dale un nombre descriptivo: `verticcal-crm-agent`
4. Copia la API key completa (no la pierda)

**Formato esperado:**
```
sk-or-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## Paso 3: Configurar en tu proyecto

### Opción A: Variables de entorno (.env)

1. Abre o crea `backend/.env`:

```dotenv
# Pipedrive
PIPEDRIVE_API_KEY=your_pipedrive_api_key_here

# Open Router
OPEN_ROUTER_API_KEY=sk-or-xxxxx...
OPEN_ROUTER_MODEL=openai/gpt-3.5-turbo
```

### Opción B: En n8n (Recomendado)

1. Abre n8n: **[http://localhost:5678](http://localhost:5678)**
2. Ve a **Settings → Credentials** (esquina superior izquierda)
3. Haz clic en **"Create new"**
4. Selecciona **"Generic Credentials"**
5. Configura así:

```
Name:       Open Router API Key
Auth Type:  Bearer
API Key:    sk-or-xxxxx...
```

6. Guarda

Luego en el nodo HTTP, selecciona esta credencial.

---

## Modelos disponibles en Open Router

| Modelo | ID | Costo/1K tokens | Velocidad | Recomendado |
|--------|----|-----------------|-----------| ----------- |
| GPT-4 Turbo | `openai/gpt-4-turbo-preview` | $0.01 | Muy lenta | ⭐⭐⭐⭐⭐ |
| GPT-3.5 Turbo | `openai/gpt-3.5-turbo` | $0.0005 | Rápida | ⭐⭐⭐⭐ |
| Claude 3 Opus | `anthropic/claude-3-opus` | $0.015 | Lenta | ⭐⭐⭐⭐⭐ |
| Claude 3 Sonnet | `anthropic/claude-3-sonnet` | $0.003 | Media | ⭐⭐⭐⭐ |
| Llama 2 70B | `meta-llama/llama-2-70b-chat` | $0.0007 | Rápida | ⭐⭐⭐ |

**Recomendación para este proyecto:**
- **Desarrollo**: `openai/gpt-3.5-turbo` (más barato, suficientemente bueno)
- **Producción**: `openai/gpt-4-turbo-preview` (mejor calidad)

---

## Cambiar el modelo

### En `backend/.env`:
```dotenv
OPEN_ROUTER_MODEL=openai/gpt-4-turbo-preview
```

### En el workflow n8n:
1. Abre el nodo **"Open Router API Request"**
2. En el campo **"model"**, cambia:

```
= $env.OPEN_ROUTER_MODEL || 'openai/gpt-4-turbo-preview'
```

---

## Monitorizar gastos

1. Ve a **[https://openrouter.ai/keys](https://openrouter.ai/keys)**
2. Haz clic en tu API key
3. Verás:
   - Total de tokens usados
   - Costo acumulado
   - Modelos utilizados
   - Historial de requests

**Presupuesto recomendado:**
- **Testing**: $1-5 USD
- **Demo pequeña (20-30 llamadas)**: $10-20 USD
- **Producción (1000 llamadas/mes)**: $50-100 USD

---

## Solución de problemas

### Error: "401 Unauthorized"
**Causa**: API key inválida o vencida
**Solución**: 
1. Ve a [https://openrouter.ai/keys](https://openrouter.ai/keys)
2. Crea una nueva API key
3. Actualiza en `backend/.env` y n8n

### Error: "429 Too Many Requests"
**Causa**: Límite de rate alcanzado
**Solución**:
1. Espera 1 minuto antes de reintentar
2. En producción, agrega retry automático en n8n

### Error: "Model not found"
**Causa**: Nombre del modelo incorrecto
**Solución**:
1. Ve a [https://openrouter.ai/docs/models](https://openrouter.ai/docs/models)
2. Copia exactamente el ID del modelo
3. Actualiza en `OPEN_ROUTER_MODEL`

---

## Ejemplo: Cambiar a GPT-4 Turbo

### Paso 1: Actualizar `.env`
```dotenv
OPEN_ROUTER_API_KEY=sk-or-xxxxx...
OPEN_ROUTER_MODEL=openai/gpt-4-turbo-preview
```

### Paso 2: Reiniciar FastAPI
```bash
python backend/main.py
```

### Paso 3: Actualizar n8n (si aplica)
En el nodo HTTP "Open Router API Request", verifica que use `$env.OPEN_ROUTER_MODEL`.

### Paso 4: Testear
```bash
# En n8n, ve a Chat y escribe:
"Crea un contacto llamado Juan Pérez con email juan@ejemplo.com"
```

---

## Integración con n8n (Workflow)

El workflow incluye un nodo HTTP que conecta con Open Router:

```
Chat Trigger → Chat Memory → AI Tools → [HTTP: Open Router] → HTTP Endpoints (FastAPI)
```

**Configuración en n8n:**

Nodo: **HTTP - Open Router Request**

```
Method:     POST
URL:        https://openrouter.ai/api/v1/chat/completions
Auth:       Bearer Token (OPEN_ROUTER_API_KEY)

Headers:
- Authorization: Bearer {API_KEY}
- HTTP-Referer: https://verticcal-crm-agent.local
- X-Title: Verticcal CRM Agent

Body:
{
  "model": "openai/gpt-3.5-turbo",
  "messages": [...],
  "tools": [...],
  "tool_choice": "auto",
  "temperature": 0.7
}
```

---

## Comparación: OpenAI vs Open Router

| Aspecto | OpenAI Directo | Open Router |
|---------|---|---|
| Setup | ⭐⭐⭐⭐⭐ Más fácil | ⭐⭐⭐⭐ Fácil |
| Precio | ⭐⭐⭐ Más caro | ⭐⭐⭐⭐⭐ Más barato |
| Modelos | ⭐ Solo OpenAI | ⭐⭐⭐⭐⭐ 30+ modelos |
| Fallback | ❌ No | ✅ Automático |
| Dashboard | ⭐⭐⭐⭐ Bueno | ⭐⭐⭐⭐ Bueno |
| Latencia | ⭐⭐⭐⭐⭐ Muy rápido | ⭐⭐⭐⭐ Rápido |
| Soporte | ⭐⭐⭐⭐⭐ Excelente | ⭐⭐⭐ Bueno |

**Veredicto**: Open Router es ideal para este proyecto. Más barato, misma calidad.

---

## Next Steps

1. ✅ Registrate en Open Router
2. ✅ Obtén tu API key
3. ✅ Configura `.env` con la API key
4. ✅ Importa el workflow `verticcal-crm-agent-workflow-openrouter.json` en n8n
5. ✅ Testea los 3 casos de uso

**¿Preguntas?** Ver documentación completa en `docs/reference/FAQ.md`
