# ⚡ Quick Start - 5 Minutos

## 1️⃣ Prerequisitos
- Python 3.11+
- pip
- n8n (o Docker)

## 2️⃣ Obtener Credenciales

### Pipedrive API Key (Obligatorio)
1. Ir a https://app.pipedrive.com/settings/personal/api
2. Copiar el **API Token**

### Open Router API Key (RECOMENDADO - Más barato) 💰
1. Ir a https://openrouter.ai/keys
2. Crear una nueva API key
3. Copiar el token (comienza con `sk-or-`)

### OpenAI API Key (Alternativa, opcional)
1. Ir a https://platform.openai.com/api-keys
2. Crear una nueva key (si usas OpenAI directo)

## 3️⃣ Clonar y Configurar

```bash
# Clonar (si tienes Git)
git clone <repo-url>
cd  -crm-agent

# O descargar ZIP y descomprimir
```

## 4️⃣ Instalar Dependencias

**Windows (PowerShell):**
```powershell
.\setup.ps1
# O manual:
cd backend
pip install -r requirements.txt
cd ..
```

**Mac/Linux:**
```bash
chmod +x setup.sh
./setup.sh
# O manual:
cd backend
pip install -r requirements.txt
cd ..
```

## 5️⃣ Configurar Variables

```bash
# Editar backend/.env
# Windows: notepad backend\.env
# Mac/Linux: nano backend/.env

# Agregar SIEMPRE:
PIPEDRIVE_API_KEY=your_actual_key

# Agregar UNA de las siguientes (Open Router recomendado):
# Opción 1: Open Router (RECOMENDADO)
OPEN_ROUTER_API_KEY=sk-or-xxxxx
OPEN_ROUTER_MODEL=openai/gpt-3.5-turbo

# Opción 2: OpenAI directo (alternativa)
OPENAI_API_KEY=sk-xxxxx
```

## 6️⃣ Ejecutar FastAPI

**Opción A - Directo:**
```bash
cd backend
python main.py
# Verá: Uvicorn running on http://0.0.0.0:8000
```

**Opción B - Docker:**
```bash
docker-compose up -d fastapi
# FastAPI en http://localhost:8000
```

## 7️⃣ Iniciar n8n

**Opción A - Directo:**
```bash
# En otra terminal
n8n start
# Abrirá: http://localhost:5678
```

**Opción B - Docker:**
```bash
docker-compose up -d n8n
# n8n en http://localhost:5678
```

## 8️⃣ Importar Flujo n8n

1. Abrir http://localhost:5678
2. Crear cuenta si es primera vez
3. Click **"Workflows"** → **"Import"**
4. Seleccionar: `n8n-workflows/ -crm-agent-workflow.json`
5. Click **"Import"**

## 9️⃣ Configurar Credenciales n8n

1. En el flujo, click en nodo **"OpenAI Chat Model"** (o "Open Router")
2. Click **"Change"** → **"New Credential"**
3. Pegar tu **API Key** (OpenAI o Open Router)
4. Click **"Save"**

## 🔟 Activar Flujo

1. Toggle **"Active"** en parte superior
2. Debería verse **AZUL**
3. ¡Listo!

## ✅ Probar

En el chat de n8n (parte superior), escribir:

```
Crea a Ana Gómez con email ana.gomez@ejemplo.com y teléfono +57 315 222 3344
```

Deberías ver:
- ✅ Contacto creado
- ✅ ID del contacto
- ✅ URL de Pipedrive

**¡Listo, felicidades! 🎉**

---

## 🔧 Troubleshooting Rápido

| Problema | Solución |
|----------|----------|
| FastAPI no inicia | Verificar: `python backend/main.py` directo |
| n8n no conecta a FastAPI | Cambiar `localhost` a `fastapi` si usas Docker |
| "Invalid OpenAI key" | Verificar key en https://platform.openai.com/api-keys |
| Chat no responde | Verificar que flujo está **Active** (azul) |
| "Contact not found" | Usar ID explícito del contacto de Pipedrive |

---

## 📖 Documentación Completa

Para más detalles, revisar:
- **docs/getting-started/README.md** - Guía principal
- **docs/testing-validation/TESTING.md** - Casos de prueba
- **docs/setup-guides/N8N_SETUP_GUIDE.md** - Configuración n8n
- **docs/deployment/DEPLOYMENT.md** - Deploy en producción

---

**¿Preguntas?** Revisar docs/getting-started/README.md → Sección Troubleshooting
