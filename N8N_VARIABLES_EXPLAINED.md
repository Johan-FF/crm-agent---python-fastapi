# ❓ Por qué las Variables de N8N no aparecen en Settings

## 📌 Respuesta Corta

Las variables de entorno en N8N **se configuran en la interfaz gráfica**, no en el JSON del workflow. El JSON solo contiene las **referencias** a esas variables (ej: `$env.OPEN_ROUTER_API_KEY`), no los valores reales.

## 🔍 Explicación Técnica

### Cómo Funcionan las Variables en N8N

```
1. Tu escribes en N8N Settings:
   OPEN_ROUTER_API_KEY = sk-or-xxxxx
   
2. N8N almacena esto en su base de datos (no en JSON)

3. En el workflow, referencias la variable:
   Authorization: Bearer={{ $env.OPEN_ROUTER_API_KEY }}
   
4. Cuando ejecutas, N8N reemplaza $env.OPEN_ROUTER_API_KEY 
   con el valor real de settings
```

### El JSON Solo Contiene Referencias

```json
{
  "headerParameters": {
    "parameters": [
      {
        "name": "Authorization",
        "value": "Bearer={{ $env.OPEN_ROUTER_API_KEY }}"  ← REFERENCIA, no valor
      }
    ]
  }
}
```

**Nota:** El JSON **nunca** debería contener valores secretos como API keys.

## ✅ Cómo Configurar Variables Correctamente

### Paso 1: En N8N UI
1. Click en **⚙️ Settings** (engranaje, esquina inferior izquierda)
2. Click en **"Variables"** (o "Environment variables")
3. Click en **"+"** (agregar nueva)
4. Ingresa:
   - **Name:** `OPEN_ROUTER_API_KEY`
   - **Value:** `sk-or-tu-api-key-aqui` (cópiala de https://openrouter.ai/keys)
5. Click en **Save**

### Paso 2: En el Workflow
Usa `$env.OPEN_ROUTER_API_KEY` para referenciarlo:

```
Authorization: Bearer={{ $env.OPEN_ROUTER_API_KEY }}
```

### Paso 3: Reinicia N8N
N8N debe reiniciarse para que lee las nuevas variables.

## 🚨 Errores Comunes

### Error 1: "Variable not found: OPEN_ROUTER_API_KEY"
**Causa:** La variable no está configurada en Settings
**Solución:** 
- Abre Settings → Variables
- Agrega la variable
- Reinicia N8N

### Error 2: "Syntax error in expression"
**Causa:** Referencia incorrecta a la variable
**Incorrecto:** `{{ $env.open_router_api_key }}` (minúsculas)
**Correcto:** `{{ $env.OPEN_ROUTER_API_KEY }}` (mayúsculas exactas)

### Error 3: Variables configuradas pero no aparecen
**Causa:** N8N no reinició después de configurarlas
**Solución:**
- Detén N8N: Ctrl+C
- Inicia N8N nuevamente: `docker run... n8n`
- Abre http://localhost:5678

## 🔄 Flujo Correcto de Configuración

```
1. Inicia N8N
   ↓
2. Abre http://localhost:5678
   ↓
3. Importa workflow JSON
   ↓
4. Abre Settings → Variables
   ↓
5. Agrega OPEN_ROUTER_API_KEY
   ↓
6. Reinicia N8N
   ↓
7. Abre workflow nuevamente
   ↓
8. Click "Deploy"
   ↓
9. ✓ ¡Funcionará!
```

## 💾 Dónde se Guardan las Variables

| Ubicación | Almacenamiento | Seguro |
|-----------|----------------|--------|
| N8N Settings UI | Base de datos de N8N | ✅ (encriptadas) |
| JSON del workflow | Archivo de texto plano | ❌ (no seguro) |
| Archivo `.env` | Archivo local | ✅ (si está en .gitignore) |
| Código fuente | Git | ❌ (nunca!) |

## 📝 Ejemplo Completo

### Configuración en Settings:
```
OPEN_ROUTER_API_KEY = sk-or-v1-abcdef123456789
OPEN_ROUTER_MODEL = openai/gpt-3.5-turbo
BACKEND_URL = http://localhost:8000
```

### Uso en Workflow (HTTP Node):
```json
{
  "headerParameters": {
    "parameters": [
      {
        "name": "Authorization",
        "value": "Bearer={{ $env.OPEN_ROUTER_API_KEY }}"
      }
    ]
  },
  "bodyParameters": {
    "parameters": [
      {
        "name": "model",
        "value": "={{ $env.OPEN_ROUTER_MODEL }}"
      }
    ]
  }
}
```

### Resultado Cuando Ejecuta:
```
Header Authorization: Bearer=sk-or-v1-abcdef123456789
Body model: openai/gpt-3.5-turbo
```

## 🛠️ Alternativa: Usar Docker con .env

Si prefieres usar archivo `.env` con Docker:

```bash
docker run -it --rm -p 5678:5678 \
    -e OPEN_ROUTER_API_KEY="$(Get-Content .env | Select-String OPEN_ROUTER_API_KEY | % { $_.Line.Split('=')[1] })" \
    n8n
```

O más simple, copia las variables:

```powershell
$env:OPEN_ROUTER_API_KEY = "tu-api-key"
docker run -it --rm -p 5678:5678 -e OPEN_ROUTER_API_KEY n8n
```

## ✨ Mejores Prácticas

1. **Nunca comitas API keys al repositorio**
   - Agrega `.env` a `.gitignore`
   - Agrega `credentials.json` a `.gitignore`

2. **Usa archivos `.env` para desarrollo local**
   ```
   .env (gitignored)
   .env.example (en repo, sin valores reales)
   ```

3. **En producción, usa variables del sistema**
   ```powershell
   docker run ... -e OPEN_ROUTER_API_KEY=$env:OPEN_ROUTER_API_KEY n8n
   ```

4. **Rota API keys regularmente**
   - Genera nuevas en OpenRouter
   - Actualiza en N8N Settings
   - Elimina las viejas

5. **Establece límites de gastos**
   - En OpenRouter: Settings → Spending Limits
   - En N8N: Logs para monitorear usage

## 📚 Referencias

- [N8N Environment Variables](https://docs.n8n.io/hosting/environment-variables/)
- [OpenRouter API Keys](https://openrouter.ai/keys)
- [Docker Environment Variables](https://docs.docker.com/compose/environment-variables/)

---

**Resumen:** Variables se configuran en N8N Settings, no en JSON. El JSON solo contiene referencias (`$env.VAR_NAME`).
