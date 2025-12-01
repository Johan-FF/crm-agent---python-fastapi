# 🚀 Guía Rápida: Conectar Nodos N8N Correctamente

## PROBLEMA: Los nodos no se conectan en N8N

Esto ocurre cuando:
1. N8N no reconoce las referencias de nodos por nombre
2. Las versiones de N8N no coinciden
3. El JSON tiene mal formato en las conexiones

## SOLUCIÓN: Conectar Manualmente en N8N

### Paso 1: Abre N8N
```
http://localhost:5678
```

### Paso 2: Importa el workflow
- Click en "+" → "Import from file"
- Selecciona: `verticcal-crm-agent-workflow.json`

### Paso 3: Conecta los Nodos Manualmente

Haz clic en el **punto pequeño** en la salida de cada nodo y arrastra hasta el siguiente:

```
1. Chat Trigger (salida) → Chat Memory (entrada)
2. Chat Memory (salida) → AI Tools (entrada)
3. AI Tools (salida) → Open Router API Request (entrada)
4. Open Router API Request (salida) → HTTP - Create Contact (entrada)
   └─ también a → HTTP - Add Note (entrada)
   └─ también a → HTTP - Update Contact (entrada)
5. HTTP - Create Contact (salida) → Chat Memory (entrada)
6. HTTP - Add Note (salida) → Chat Memory (entrada)
7. HTTP - Update Contact (salida) → Chat Memory (entrada)
```

### Paso 4: Configura Variables de Entorno

1. **Settings** (engranaje abajo a la izquierda)
2. **Variables** (o Environment)
3. Agrega:
   ```
   OPEN_ROUTER_API_KEY = tu_api_key_aqui
   ```

### Paso 5: Prueba el Workflow

1. Click en "Deploy" (esquina superior derecha)
2. Espera "Workflow active" en verde
3. Click en "Chat" (a la derecha)
4. Escribe: `Crea a Falcao García con email falcao@verticcal.com`
5. ¡Debería funcionar!

## Si sigue sin funcionar:

### Opción A: Verificar que OpenRouter esté accesible
```powershell
Invoke-RestMethod -Uri "https://openrouter.ai/api/v1/models" -Headers @{
    "Authorization" = "Bearer=tu_api_key_aqui"
}
```

### Opción B: Verificar que el backend esté corriendo
```powershell
curl http://localhost:8000/health
```

Si devuelve `{"status":"ok"}`, el backend está bien.

### Opción C: Regenerar conexiones en el JSON

Si ninguna conexión funciona, elimina todo el archivo `verticcal-crm-agent-workflow.json` y crea uno nuevo:

```powershell
# Desde la carpeta del proyecto
rm n8n-workflows/verticcal-crm-agent-workflow.json
```

Luego usa la interfaz gráfica de N8N para conectar manualmente:
- Crea 7 nodos desde cero
- Conecta manualmente cada uno
- Configura parámetros en la UI
- Exporta como JSON

## Referencia de Nodos N8N Usados:

| Nodo | ID N8N | Versión |
|------|--------|---------|
| Chat Trigger | `n8n-nodes-base.chatTrigger` | 1 |
| Chat Memory | `n8n-nodes-base.chatMemory` | 1 |
| AI Tools | `n8n-nodes-base.toolsLanguageModel` | 1 |
| HTTP Request | `n8n-nodes-base.httpRequest` | 4.1 |

## Alternativa: Usar N8N en Docker

```bash
docker run -it --rm \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8n
```

Esto asegura que N8N esté siempre actualizado y funcione igual en todos lados.
