#   CRM Agent 🤖

Sistema conversacional integrado con n8n, FastAPI y Pipedrive que permite gestionar contactos mediante Chat Agent inteligente.

## 📋 Descripción General

Este proyecto implementa un agente conversacional que interpreta órdenes naturales del usuario para:
- ✅ **Crear contactos** con nombre, email y teléfono
- ✅ **Agregar notas** a contactos existentes
- ✅ **Actualizar campos** de contactos (teléfono, estado, etc.)

### Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                         n8n                                  │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Chat Trigger → Chat Agent + Tools → Memory          │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ HTTP Request
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                      FastAPI Backend                         │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  POST /crm/contact                                   │   │
│  │  POST /crm/contact/note                              │   │
│  │  PATCH /crm/contact                                  │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ REST API
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                      Pipedrive CRM                           │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Contacts | Notes | Fields                           │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Requisitos Previos

- **Python 3.11+**
- **Node.js 18+** (para n8n)
- **Docker & Docker Compose** (opcional, para despliegue fácil)
- **Cuenta Pipedrive** (gratuita en https://www.pipedrive.com)
- **Open Router API Key** → [Obtener aquí](https://openrouter.ai/keys) ⭐ RECOMENDADO
  - Alternativa: OpenAI API Key (más caro)

## 📦 Setup Local

### 1. Clonar el Repositorio

```bash
git clone <repository-url>
cd  -crm-agent
```

### 2. Configurar Variables de Entorno

```bash
# Copiar archivo de ejemplo
cp backend/.env.example backend/.env

# Editar backend/.env y agregar:
# PIPEDRIVE_API_KEY=your_actual_api_key_here
# OPEN_ROUTER_API_KEY=sk-or-xxxxxx  (o OpenAI API Key)
```

**Obtener API Keys:**

1. **Pipedrive** → https://app.pipedrive.com/settings/personal/api
2. **Open Router** → https://openrouter.ai/keys (recomendado, más barato)
   - Alternativa: OpenAI → https://platform.openai.com/api-keys

**Guía completa de Open Router**: Ver `docs/setup-guides/OPENROUTER_SETUP.md`

### 3. Instalar Dependencias de FastAPI

```bash
cd backend
pip install -r requirements.txt
```

### 4. Ejecutar FastAPI

```bash
# Opción A: Directamente
python main.py

# Opción B: Con uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

FastAPI estará disponible en `http://localhost:8000`

### 5. Instalar y Configurar n8n

```bash
# Opción A: Local (requiere Node.js)
npm install -g n8n
n8n start

# Opción B: Docker
docker run -it --rm --name n8n -p 5678:5678 n8nio/n8n:latest
```

n8n estará disponible en `http://localhost:5678`

### 6. Importar Flujo en n8n

**Opción A: Con Open Router (RECOMENDADO)** 💰 Más barato

1. Abrir n8n en `http://localhost:5678`
2. Click en **"New Workflow"** → **"Import from File"**
3. Seleccionar `n8n-workflows/ -crm-agent-workflow-openrouter.json`
4. Completar credenciales:
   - **Open Router API Key**: Tu clave de Open Router (desde https://openrouter.ai/keys)
   - **Endpoint HTTP**: `http://localhost:8000` (si corres localmente)
5. Ver: `docs/setup-guides/OPENROUTER_SETUP.md` para instrucciones detalladas

**Opción B: Con OpenAI directo**

1. Abrir n8n en `http://localhost:5678`
2. Click en **"New Workflow"** → **"Import from File"**
3. Seleccionar `n8n-workflows/ -crm-agent-workflow.json`
4. Completar credenciales:
   - **OpenAI API Key**: Tu clave de OpenAI
   - **Endpoint HTTP**: `http://localhost:8000`
5. Activar el flujo

## 🐳 Opción: Docker Compose (Recomendado)

```bash
# En la raíz del proyecto
docker-compose up -d

# Verificar servicios
docker-compose ps

# Ver logs
docker-compose logs -f fastapi
docker-compose logs -f n8n
```

URLs después de ejecutar Docker Compose:
- **FastAPI**: `http://localhost:8000`
- **n8n**: `http://localhost:5678`

## 🧪 Casos de Uso y Prompts de Prueba

### 1️⃣ Crear Contacto

**Prompts de ejemplo:**
```
"Crea a Ana Gómez con email ana.gomez@ejemplo.com y teléfono +57 315 222 3344."
"Registra un nuevo contacto: nombre Carlos Martín, correo carlos@empresa.com, teléfono +57 320 123 4567."
"Agrega a María López, email: maria.lopez@mail.com"
"Nuevo contacto: Juan Pérez, +57 310 555 6666"
```

**Resultado esperado:**
- ✅ Contacto creado en Pipedrive
- ✅ Mensaje de confirmación con ID y URL

### 2️⃣ Agregar Nota a Contacto

**Prompts de ejemplo:**
```
"Agrega una nota a Ana Gómez: 'Cliente interesado en plan Premium'"
"Nota para Carlos Martín: 'Seguimiento pendiente para próxima semana'"
"Crea una nota en el contacto de María López diciendo: 'Pagó su factura'"
```

**Resultado esperado:**
- ✅ Nota creada en Pipedrive
- ✅ Asociada al contacto correcto

### 3️⃣ Actualizar Contacto

**Prompts de ejemplo:**
```
"Actualiza el teléfono de Ana Gómez a +57 311 999 0000"
"Marca a Carlos Martín como 'Qualified' en su estado"
"Cambia el email de María López a maria.nueva@empresa.com"
```

**Resultado esperado:**
- ✅ Campo actualizado en Pipedrive
- ✅ Confirmación de actualización

## 📋 Flujo de Uso

1. **Abre n8n** en tu navegador (`http://localhost:5678`)
2. **Activa el flujo** haciendo click en el botón de activación
3. **Abre el chat** (botón en la esquina inferior derecha)
4. **Escribe una orden** natural: "Crea un contacto llamado Juan"
5. **El agente procesa** la orden y crea el contacto en Pipedrive
6. **Recibes confirmación** con ID y enlace al contacto

## 🔍 Validaciones Automáticas

El sistema realiza validaciones automáticas:

- ✅ **Email único**: No permite duplicados
- ✅ **Email válido**: Formato correcto
- ✅ **Nombre mínimo**: Al menos 2 caracteres
- ✅ **Teléfono flexible**: Acepta formatos variados
- ✅ **Campos requeridos**: Valida parámetros obligatorios

## 🛠️ Troubleshooting

### FastAPI no inicia
```bash
# Verifica que el puerto 8000 esté disponible
lsof -i :8000  # En Mac/Linux
netstat -ano | findstr :8000  # En Windows

# Si está ocupado, cambia el puerto:
python main.py --port 8001
```

### n8n no conecta a FastAPI
1. Verifica que FastAPI esté corriendo: `http://localhost:8000/docs`
2. En n8n, verifica que la URL sea `http://localhost:8000`
3. Revisa los logs: `docker-compose logs fastapi`

### Error de API key
1. Verifica que `backend/.env` existe y tiene valores
2. Copia la API key correctamente (sin espacios)
3. Reinicia FastAPI después de cambiar `.env`

## 📚 Documentación Completa

- **Getting Started**: `docs/getting-started/` (este archivo)
- **Setup Guides**: `docs/setup-guides/` (instrucciones técnicas)
- **Testing**: `docs/testing-validation/TESTING.md`
- **Deployment**: `docs/deployment/` (producción)
- **Architecture**: `docs/architecture/` (diseño técnico)
- **Reference**: `docs/reference/` (FAQs, índices)

## 🎯 Siguiente Paso

→ Lee: `docs/getting-started/QUICKSTART.md` para setup rápido en 5 minutos

