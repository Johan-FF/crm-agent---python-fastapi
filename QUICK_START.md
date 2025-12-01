# ⚡ Quick Start: N8N + Verticcal CRM Agent

## 🎯 Objetivo
Ejecutar un flujo N8N que:
1. Reciba un prompt: "Crea a Falcao García con email falcao@verticcal.com"
2. Envíe a OpenRouter (GPT-3.5-turbo)
3. Extraiga nombre, email, teléfono
4. Cree el contacto en tu API local

## ✅ Requisitos (5 minutos)

### 1. Backend ejecutándose
```powershell
cd verticcal-crm-agent
npm start
# Debería mostrar: ✓ Server running on http://localhost:8000
```

### 2. PostgreSQL ejecutándose
```powershell
docker-compose up -d
# O usa PostgreSQL instalado localmente
```

### 3. API Key de OpenRouter
1. Ve a https://openrouter.ai/signup (o login si ya tienes cuenta)
2. Copia tu API Key desde https://openrouter.ai/keys
3. Guárdala en un lugar seguro

## 🚀 Inicio Rápido (3 pasos)

### Paso 1: Iniciar N8N
```powershell
# Si tienes Docker instalado:
docker run -it --rm -p 5678:5678 `
    -e OPEN_ROUTER_API_KEY="sk-or-tu-api-key-aqui" `
    n8n
```

**Alternativa sin Docker:**
- Descarga N8N desde https://n8n.io/download
- Ejecuta: `npx n8n start`

### Paso 2: Abre N8N en tu navegador
```
http://localhost:5678
```

### Paso 3: Importa el Workflow
1. Click en "+" en la esquina superior izquierda
2. Selecciona "Import from file"
3. Elige: `n8n-workflows/verticcal-crm-agent-workflow.json`
4. Click en "Import"

## 🔌 Conecta los Nodos Manualmente

Si los nodos no aparecen conectados:

1. Haz clic en el punto pequeño (●) de salida del **Chat Trigger**
2. Arrastra hasta el punto de entrada del **Chat Memory**
3. Repite para las siguientes conexiones:
   ```
   Chat Trigger → Chat Memory
   Chat Memory → AI Tools
   AI Tools → Open Router API Request
   Open Router API Request → HTTP - Create Contact
   Open Router API Request → HTTP - Add Note
   Open Router API Request → HTTP - Update Contact
   HTTP - Create Contact → Chat Memory
   HTTP - Add Note → Chat Memory
   HTTP - Update Contact → Chat Memory
   ```

## ⚙️ Configura las Variables (IMPORTANTE)

1. Click en el **ícono de engranaje** (⚙️) en la esquina inferior izquierda
2. Haz click en **"Variables"** (o "Environment")
3. Agrega esta variable:
   ```
   OPEN_ROUTER_API_KEY = sk-or-tu-api-key-aqui
   ```

## ✨ Prueba el Flujo

1. Click en **"Deploy"** (esquina superior derecha)
2. Espera a ver "Workflow active" en verde
3. Click en el **Chat icon** (💬) a la derecha
4. Escribe el siguiente prompt:
   ```
   Crea a Falcao García con correo falcao@verticcal.com y teléfono +57 300 123 4567
   ```
5. Presiona Enter

**Resultado esperado:**
```
✓ Contacto Falcao García creado exitosamente
✓ Email: falcao@verticcal.com
✓ Teléfono: +57 300 123 4567
```

## 🐛 Troubleshooting

### Error: "Connection refused" en HTTP nodes
- Verifica que el backend esté corriendo: `http://localhost:8000/health`
- Si devuelve `{"status":"ok"}`, está bien

### Error: "401 Unauthorized" en OpenRouter
- Verifica tu API Key es correcta en https://openrouter.ai/keys
- Recopia en N8N Settings → Variables

### Error: "Variable not found: OPEN_ROUTER_API_KEY"
- Verifica que configuraste la variable en Settings → Variables
- N8N debe estar reiniciado después de agregar variables

### Los nodos no se conectan
- Conecta manualmente arrastrando y soltando
- Usa el documento `N8N_MANUAL_SETUP.md` para referencia visual

## 📚 Documentación

- `N8N_SETUP.md` - Guía detallada de setup
- `N8N_ENVIRONMENT_SETUP.md` - Configuración de variables
- `N8N_MANUAL_SETUP.md` - Conexión manual de nodos
- `API_ENDPOINTS.md` - Documentación de endpoints de la API

## 💰 Costos

OpenRouter usa modelos de pago:
- **gpt-3.5-turbo**: ~$0.0015 por 1K tokens (muy barato)
- **gpt-4**: ~$0.03 por 1K tokens (más caro pero más potente)

Recomendación: Usa gpt-3.5-turbo para empezar, es suficiente y barato.

## 🎉 ¡Listo!

Tu sistema está completamente funcional. Ahora puedes:
- Crear contactos con prompts en lenguaje natural
- Actualizar información de contactos
- Agregar notas a contactos
- Sincronizar automáticamente con Pipedrive

---

**¿Problemas?** Revisa los documentos en la carpeta `n8n-workflows/`
