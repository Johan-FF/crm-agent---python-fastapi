# 📖 Guía de Importación del Flujo n8n

## Pasos para Importar el Flujo en n8n

### 1. Acceder a n8n
- Abrir `http://localhost:5678` en el navegador
- Si es primera vez, crear una cuenta

### 2. Importar el Flujo
1. Click en **"Workflows"** (menú superior)
2. Click en **"Import"** o **"Import from File"**
3. Seleccionar el archivo: `n8n-workflows/verticcal-crm-agent-workflow.json`
4. Click en **"Import"**

El flujo se creará y abrirá automáticamente.

### 3. Configurar Credenciales

Antes de activar, necesitas configurar:

#### 3.1 OpenAI API Key
1. En el panel superior, click en **"Credentials"** o dentro del nodo **"OpenAI Chat Model"**
2. Click en **"New Credential"** → Seleccionar **"OpenAI API"**
3. Ingresar tu API Key de OpenAI (obtén una en https://platform.openai.com/api-keys)
4. Click en **"Save"**

#### 3.2 Verificar URL de FastAPI
- En los nodos HTTP (Create Contact, Add Note, Update Contact)
- Verificar que la URL sea `http://localhost:8000` (si está corriendo localmente)
- Si despliegas FastAPI en otro servidor, cambiar la URL en cada nodo HTTP

### 4. Configurar Chat Trigger (Opcional)

Si deseas exponer el chat públicamente:
1. Click en el nodo **"Chat Trigger"**
2. En la sección "General", copiar la URL generada
3. Esta es la URL pública para acceder al chat

### 5. Activar el Flujo

1. En la parte superior derecha, ver el toggle **"Active"**
2. Hacer click para activar el flujo (debería verse azul)
3. El flujo ahora escuchará mensajes

### 6. Pruebas Rápidas

Ahora puedes:

1. **Crear contacto:**
   ```
   Crea a Ana Gómez con email ana.gomez@ejemplo.com y teléfono +57 315 222 3344
   ```

2. **Agregar nota:**
   ```
   Agrega una nota a Ana Gómez: 'Cliente interesado en plan Premium'
   ```

3. **Actualizar contacto:**
   ```
   Actualiza el teléfono de Ana Gómez a +57 311 999 0000
   ```

## 🐛 Troubleshooting

### "Error connecting to FastAPI"
- Verificar que FastAPI está corriendo: `curl http://localhost:8000/health`
- En Docker, cambiar `localhost` por `fastapi`

### "Invalid OpenAI credentials"
- Verificar que la API key es válida en https://platform.openai.com/api-keys
- Regenerar si es necesario

### Chat no responde
- Verificar que el flujo está **Active** (toggle azul)
- Revisar los logs: Click en **"Execution History"** en el flujo

### ContactID no reconocido
- Si el agente no puede buscar el contacto por nombre automáticamente, solicitar el ID
- Ir a Pipedrive y copiar el ID del contacto
- Pedir al agente: "Agrega nota al contacto ID 12345: ..."

## 📌 Notas Importantes

- El flujo usa **GPT-4** de OpenAI (también funciona con GPT-3.5-turbo)
- La URL de FastAPI debe ser accesible desde n8n
- Los logs se guardan en la "Execution History" del flujo
- El Chat Memory mantiene el historial durante la sesión

## 🔄 Próximos Pasos

1. Activar el flujo
2. Probar los 3 casos de uso
3. Revisar logs si hay errores
4. Verificar contactos en Pipedrive
5. Documentar cualquier issue encontrado
