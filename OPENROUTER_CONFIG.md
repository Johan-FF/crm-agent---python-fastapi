# 🔑 Configuración de OpenRouter en N8N

## ⚠️ ERROR ACTUAL: "The resource you are requesting could not be found"

Este error significa que **la API key de OpenRouter NO está configurada** en n8n.

---

## ✅ Solución: Configurar Variables de Entorno

### Paso 1: Obtener API Key de OpenRouter

1. Ve a **https://openrouter.ai**
2. Inicia sesión (o regístrate si es tu primera vez)
3. Ve a **Keys**: https://openrouter.ai/keys
4. Haz clic en **"Create Key"**
5. Copia la API key (formato: `sk-or-v1-xxxxxxxxxxxxxxxx`)

---

### Paso 2: Configurar en N8N

#### Opción A: Variables de Entorno en N8N (Recomendado)

1. Abre n8n: `http://localhost:5678`
2. Haz clic en tu **foto de perfil** (esquina superior derecha)
3. Selecciona **"Settings"**
4. En el menú lateral, haz clic en **"Variables"**
5. Haz clic en **"+ Add Variable"**
6. Agrega estas dos variables:

**Variable 1:**
```
Key:   OPEN_ROUTER_API_KEY
Value: sk-or-v1-xxxxxxxxxxxxxxxx
Type:  String
```

**Variable 2:**
```
Key:   OPEN_ROUTER_MODEL
Value: openai/gpt-4-turbo
Type:  String
```

7. Haz clic en **"Save"**

---

#### Opción B: Variables de Entorno del Sistema (Si usas Docker)

Edita `docker-compose.yml` y agrega:

```yaml
services:
  n8n:
    environment:
      - OPEN_ROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxx
      - OPEN_ROUTER_MODEL=openai/gpt-4-turbo
```

Luego reinicia:
```powershell
docker-compose down
docker-compose up -d
```

---

#### Opción C: Archivo .env (Si ejecutas n8n local)

Crea o edita `.env` en la raíz de n8n:

```env
OPEN_ROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxx
OPEN_ROUTER_MODEL=openai/gpt-4-turbo
```

Reinicia n8n:
```powershell
# Si usas npm
pkill n8n
npx n8n
```

---

## 🎯 Modelos GPT-4 Disponibles en OpenRouter

| Modelo | ID en OpenRouter | Costo | Velocidad |
|--------|------------------|-------|-----------|
| **GPT-4 Turbo** | `openai/gpt-4-turbo` | $10/1M tokens | Rápida ⚡ |
| GPT-4 Turbo Preview | `openai/gpt-4-turbo-preview` | $10/1M tokens | Rápida ⚡ |
| GPT-4 | `openai/gpt-4` | $30/1M tokens | Lenta 🐌 |
| GPT-4 32k | `openai/gpt-4-32k` | $60/1M tokens | Lenta 🐌 |

**Recomendado**: `openai/gpt-4-turbo` (mejor balance precio/velocidad)

El workflow ahora usa por defecto: **`openai/gpt-4-turbo`**

---

## 🧪 Verificar que Funciona

### Test 1: Verificar API Key

```powershell
# En PowerShell, prueba directamente OpenRouter
$headers = @{
    "Authorization" = "Bearer sk-or-v1-TU_API_KEY_AQUI"
    "Content-Type" = "application/json"
    "HTTP-Referer" = "https://verticcal-crm-agent.local"
}

$body = @{
    model = "openai/gpt-4-turbo"
    messages = @(
        @{
            role = "user"
            content = "Hola, responde con 'OK' si funcionas"
        }
    )
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://openrouter.ai/api/v1/chat/completions" `
    -Method POST `
    -Headers $headers `
    -Body $body
```

**Respuesta esperada**:
```json
{
  "id": "chatcmpl-xxxxx",
  "model": "openai/gpt-4-turbo",
  "choices": [{
    "message": {
      "role": "assistant",
      "content": "OK"
    }
  }]
}
```

---

### Test 2: Verificar en N8N

1. Abre el workflow en n8n
2. Haz clic en el nodo **"OpenAI Model (via OpenRouter)"**
3. Verifica que el campo **"API Key"** muestre: `={{ $vars.OPEN_ROUTER_API_KEY }}`
4. Verifica que el campo **"Base URL"** sea: `https://openrouter.ai/api/v1`
5. Verifica que el campo **"Model"** sea: `={{ $vars.OPEN_ROUTER_MODEL ?? 'openai/gpt-4-turbo' }}`

---

## 🔍 Troubleshooting

### Error: "The resource you are requesting could not be found"

**Causa 1**: API key no configurada
- ✅ **Solución**: Configurar `OPEN_ROUTER_API_KEY` en n8n Settings → Variables

**Causa 2**: API key inválida o vencida
- ✅ **Solución**: Crear nueva API key en https://openrouter.ai/keys

**Causa 3**: Modelo no existe
- ✅ **Solución**: Cambiar a `openai/gpt-4-turbo` (ya corregido en el workflow)

---

### Error: "401 Unauthorized"

**Causa**: API key incorrecta

**Solución**:
1. Ve a https://openrouter.ai/keys
2. Verifica que la key esté activa
3. Copia exactamente (incluye el `sk-or-v1-` al inicio)
4. Actualiza en n8n Variables

---

### Error: "429 Too Many Requests"

**Causa**: Límite de rate alcanzado

**Solución**:
1. Espera 1 minuto
2. Verifica tu saldo en https://openrouter.ai/credits
3. Agrega créditos si es necesario

---

## 💰 Costos Estimados

### Para la Prueba Técnica (GPT-4 Turbo)

| Actividad | Tokens | Costo Aprox |
|-----------|--------|-------------|
| 1 conversación (crear contacto) | ~500 tokens | $0.005 |
| 3 casos de uso completos | ~1,500 tokens | $0.015 |
| 10 pruebas + demo | ~5,000 tokens | $0.05 |
| **Total estimado** | **~5K tokens** | **$0.05 USD** |

**Recomendación**: Agrega $5-10 USD de créditos para tener suficiente margen.

---

## 📝 Checklist de Configuración

- [ ] API key obtenida de https://openrouter.ai/keys
- [ ] Variable `OPEN_ROUTER_API_KEY` configurada en n8n
- [ ] Variable `OPEN_ROUTER_MODEL` configurada (opcional, usa default)
- [ ] Workflow reimportado
- [ ] Workflow activado
- [ ] Test de chat realizado exitosamente

---

## 🎬 Siguiente Paso

Una vez configuradas las variables:

1. **Reimporta** el workflow actualizado
2. **Activa** el workflow
3. **Prueba** con:
   ```
   Crea a Falcao García con correo falcao@verticcal.com y teléfono +57 300 123 4567
   ```

Deberías ver:
```
✅ Contacto creado exitosamente

**ID**: 1
**Nombre**: Falcao García
**Email**: falcao@verticcal.com
**Teléfono**: +57 300 123 4567
```

---

## 🆘 Soporte

Si sigues teniendo problemas:

1. Verifica logs de n8n: Settings → Log Streaming
2. Revisa ejecuciones: Executions (menú lateral)
3. Verifica que FastAPI esté corriendo: `http://localhost:8000/health`
4. Prueba la API key directamente con el script de PowerShell arriba

---

**Última actualización**: Workflow configurado con `openai/gpt-4-turbo` ✅
