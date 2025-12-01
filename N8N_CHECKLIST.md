# ✅ Checklist de Configuración N8N

Usa este checklist para verificar que todo esté configurado correctamente.

## 📋 Pre-requisitos (antes de iniciar N8N)

- [ ] Backend corriendo en `http://localhost:8000`
  - Prueba: `curl http://localhost:8000/health`
  - Debe devolver: `{"status":"ok"}`

- [ ] PostgreSQL corriendo (Docker o local)
  - Prueba: Intenta conectar con pgAdmin o psql

- [ ] Docker instalado (si usas N8N en Docker)
  - Prueba: `docker --version`

- [ ] API Key de OpenRouter obtenida
  - Ve a: https://openrouter.ai/keys
  - Copia la API key (inicia con `sk-or-`)

## 🚀 Iniciar N8N

### Opción 1: Con Docker (recomendado)
```powershell
# Ejecuta este comando en PowerShell:
docker run -it --rm -p 5678:5678 `
    -e OPEN_ROUTER_API_KEY="tu-api-key-aqui" `
    n8n
```

- [ ] N8N inicia sin errores
- [ ] Aparece: `Server is now listening...`
- [ ] Puedes acceder a: `http://localhost:5678`

### Opción 2: Sin Docker
```powershell
# Instala N8N globalmente
npm install -g n8n

# Inicia N8N
n8n start
```

- [ ] N8N inicia sin errores
- [ ] Aparece URL de acceso

## 🌐 Acceso a N8N UI

- [ ] Abre `http://localhost:5678` en tu navegador
- [ ] Ves la pantalla principal de N8N
- [ ] Puedes crear workflows

## 📥 Importar Workflow

- [ ] Click en el ícono **"+"** (esquina superior izquierda)
- [ ] Selecciona **"Import from file"**
- [ ] Navegas a: `n8n-workflows/verticcal-crm-agent-workflow.json`
- [ ] Haces click en **"Import"**
- [ ] El workflow se carga sin errores

## 🔍 Verificar Nodos

- [ ] Ves estos 7 nodos en el canvas:
  - [ ] Chat Trigger
  - [ ] Chat Memory
  - [ ] AI Tools
  - [ ] Open Router API Request
  - [ ] HTTP - Create Contact
  - [ ] HTTP - Add Note
  - [ ] HTTP - Update Contact

- [ ] Los nodos tienen posiciones visuales diferentes
- [ ] No hay ningún ícono de error rojo (❌) en los nodos

## 🔌 Verificar Conexiones

- [ ] Los nodos están conectados con líneas:
  - [ ] Chat Trigger → Chat Memory
  - [ ] Chat Memory → AI Tools
  - [ ] AI Tools → Open Router API Request
  - [ ] Open Router → HTTP nodes (x3)
  - [ ] HTTP nodes → Chat Memory

### Si no están conectados:
- [ ] Haz clic en el punto pequeño (●) de salida de **Chat Trigger**
- [ ] Arrastra hasta el punto de entrada de **Chat Memory**
- [ ] Suelta el mouse
- [ ] Repite para cada conexión faltante

## ⚙️ Configurar Variables (IMPORTANTE)

- [ ] Haz click en **⚙️ Settings** (engranaje, esquina inferior izquierda)
- [ ] Busca **"Variables"** o **"Environment"**
- [ ] Haz click en **"+"** para agregar nueva variable
- [ ] Configura:
  - [ ] **Name:** `OPEN_ROUTER_API_KEY`
  - [ ] **Value:** `tu-api-key-aqui` (copiar de https://openrouter.ai/keys)
  - [ ] **Save**

- [ ] Ves la variable listada:
  ```
  OPEN_ROUTER_API_KEY = sk-or-... (valor oculto)
  ```

## 🔄 Reiniciar N8N (después de agregar variables)

- [ ] Detén N8N: `Ctrl+C` en la terminal
- [ ] Espera 5 segundos
- [ ] Reinicia N8N: `docker run...` o `n8n start`
- [ ] Abre nuevamente `http://localhost:5678`

## 🧪 Prueba del Workflow

### Antes de probar:
- [ ] Click en **"Deploy"** (esquina superior derecha)
- [ ] Ves un indicador verde: **"Workflow active"** o **"Running"**
- [ ] Espera 3-5 segundos

### Ejecutar prueba:
- [ ] Haz click en **💬 Chat** (ícono de chat a la derecha)
- [ ] Se abre un panel de chat
- [ ] Escribes este prompt:
  ```
  Crea a Falcao García con email falcao@verticcal.com y teléfono +57 300 123 4567
  ```
- [ ] Presionas **Enter** (o Click "Send")

### Resultado esperado:
- [ ] El mensaje se envía (ves tu prompt en la ventana)
- [ ] Aparece un indicador de "cargando" (spinner)
- [ ] Después de 3-10 segundos, ves una respuesta:
  ```
  ✓ Contacto Falcao García creado exitosamente
  ✓ Email: falcao@verticcal.com
  ✓ Teléfono: +57 300 123 4567
  ```

## 🐛 Debugging (si algo falla)

### En el Chat:
- [ ] Si ves un error rojo, **anota el mensaje completo**
- [ ] Abre **Logs** (Settings → Logs)
- [ ] Busca el error en los logs

### Errores Comunes:

**❌ "Variable not found: OPEN_ROUTER_API_KEY"**
- [ ] Abre Settings → Variables
- [ ] Verifica que la variable esté presente
- [ ] Si no, agrégala nuevamente
- [ ] Reinicia N8N

**❌ "Connection refused" en HTTP node**
- [ ] Verifica backend: `curl http://localhost:8000/health`
- [ ] Si no responde, inicia el backend en otra terminal

**❌ "401 Unauthorized" en OpenRouter**
- [ ] Verifica API Key en: https://openrouter.ai/keys
- [ ] Copia la key completa (sin espacios)
- [ ] Actualiza en N8N Settings → Variables

**❌ "Nodos desconectados"**
- [ ] Arrastra desde punto de salida (●) de un nodo
- [ ] Suelta en punto de entrada (●) del siguiente
- [ ] Verifica que la línea sea visible

## 📊 Verificación Final

- [ ] Backend responde: `http://localhost:8000/health` ✓
- [ ] N8N está accesible: `http://localhost:5678` ✓
- [ ] Workflow importado correctamente ✓
- [ ] Todos los 7 nodos visibles ✓
- [ ] Todas las conexiones presentes ✓
- [ ] Variables configuradas ✓
- [ ] Workflow está en estado "Active" (deploy exitoso) ✓
- [ ] Chat responde correctamente ✓

## 🎉 ¡Listo!

Si marcaste todos los boxes arriba, **tu sistema está 100% funcional**.

Ahora puedes:
- ✅ Crear contactos con prompts en lenguaje natural
- ✅ Actualizar información de contactos
- ✅ Agregar notas a contactos
- ✅ Los datos se sincronizan automáticamente con Pipedrive

## 📞 Soporte

Si algo no funciona después de este checklist:

1. **Revisa N8N_VARIABLES_EXPLAINED.md** - explicación detallada de variables
2. **Revisa N8N_MANUAL_SETUP.md** - conexión manual de nodos
3. **Revisa los logs** - Settings → Logs en N8N
4. **Consulta documentación oficial:**
   - N8N Docs: https://docs.n8n.io
   - OpenRouter Docs: https://openrouter.ai/docs

---

**Última actualización:** Noviembre 30, 2025
