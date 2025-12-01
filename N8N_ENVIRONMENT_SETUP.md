# Variables de Entorno para N8N

Antes de ejecutar el workflow, debes configurar estas variables en N8N.

## Pasos en N8N:

1. **Ve a Settings** (ícono de engranaje en la esquina inferior izquierda)
2. **Selecciona "Environment"** 
3. **Agrega estas variables:**

```
OPEN_ROUTER_API_KEY = tu_api_key_aqui
OPEN_ROUTER_MODEL = openai/gpt-3.5-turbo
```

## Obtener API Key de OpenRouter:

### Opción 1: Si aún no tienes cuenta

1. Ve a https://openrouter.ai/signup
2. Crea una cuenta (puedes usar Google, GitHub, etc.)
3. Verifica tu email
4. Ve a https://openrouter.ai/keys
5. Copia la API key que aparece

### Opción 2: Si ya tienes cuenta

1. Ve a https://openrouter.ai/keys
2. Si no hay keys, haz clic en "Create"
3. Copia la API key

## Verificar que las Variables Están Configuradas:

En el nodo "Open Router API Request", verifica que puedas ver:
- `Authorization: Bearer={{ $env.OPEN_ROUTER_API_KEY }}`
- `model: ={{ $env.OPEN_ROUTER_MODEL || 'openai/gpt-3.5-turbo' }}`

Si ves en rojo que no encuentra la variable, significa que no está configurada correctamente.

## Alternativa: Hardcodear la API Key (no recomendado para producción)

Si prefieres por ahora, puedes reemplazar en el nodo "Open Router API Request":

Cambiar esto:
```
Authorization: Bearer={{ $env.OPEN_ROUTER_API_KEY }}
```

Por esto:
```
Authorization: Bearer=sk-or-xxx-xxxxxx-xxxxx (tu api key real)
```

Pero esto queda guardado en el JSON, así que **no lo hagas si vas a compartir el workflow**.

## Costos en OpenRouter:

OpenRouter actúa como intermediario que te permite usar varios modelos:
- **openai/gpt-3.5-turbo**: ~$0.0015 por 1K tokens
- **openai/gpt-4**: ~$0.03 por 1K tokens  
- **meta-llama/llama-2-70b**: ~$0.0009 por 1K tokens

Establece un límite de gasto en tu cuenta para no sorpresas.
