# ❓ Preguntas Frecuentes (FAQ)

## 🚀 Setup y Configuración

### P: ¿Por dónde empiezo?
**R:** Leer `docs/getting-started/QUICKSTART.md` - Te guía en 10 pasos simples en ~5 minutos.

### P: ¿Es obligatorio usar Docker?
**R:** No. Puedes instalar FastAPI y n8n localmente directamente:
```bash
pip install -r backend/requirements.txt
python backend/main.py

# En otra terminal
n8n start
```

### P: ¿Qué versión de Python necesito?
**R:** Python 3.11 o superior. Verifica con:
```bash
python --version
```

### P: ¿Dónde obtengo la API key de Pipedrive?
**R:** 
1. Crear cuenta gratis en https://www.pipedrive.com
2. Ir a Settings → Personal → API
3. Copiar el API Token
4. Pegarlo en `backend/.env`

### P: ¿Necesito tarjeta de crédito?
**R:** No, Pipedrive tiene plan gratuito sin requerimientos de pago.

---

## 💰 Costes

### P: ¿Tiene algún costo usar este sistema?
**R:** No directamente:
- **FastAPI**: Gratuito
- **Pipedrive**: Gratuito (plan básico)
- **n8n**: Gratuito (auto-hosted)
- **OpenAI API**: Debes pagar por uso (cuesta fracciones de centavo por request)

### P: ¿Cuánto cuesta OpenAI?
**R:** Aprox:
- GPT-4: $0.03 por 1K tokens (muy barato para este use case)
- GPT-3.5: $0.001 por 1K tokens (aún más barato)
- Usar: `gpt-3.5-turbo` en n8n para ahorrar

### P: ¿Cuánto cuesta Open Router?
**R:** Mucho más barato:
- GPT-3.5: $0.0005 por 1K tokens (50x más barato que OpenAI)
- GPT-4: $0.01 por 1K tokens (5x más barato que OpenAI)
- Ver `docs/setup-guides/OPENROUTER_SETUP.md` para más detalles

---

## 🔧 Problemas Técnicos

### P: FastAPI no inicia. Error: "Address already in use"
**R:** El puerto 8000 está ocupado. Opciones:
```bash
# Opción 1: Matar proceso en puerto 8000 (Windows)
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Opción 2: Usar puerto diferente
uvicorn main:app --port 8001

# Opción 3: Encontrar qué usa el puerto
lsof -i :8000  # Mac/Linux
```

### P: n8n no se conecta a FastAPI (error 500 en HTTP nodes)
**R:** Cambiar URL según tu setup:
- **Local:** `http://localhost:8000`
- **Docker:** `http://fastapi:8000` (nombre del servicio)
- **Desplegado:** `https://your-api.com`

### P: "Invalid OpenAI API Key" en n8n
**R:**
1. Verificar que copió toda la key completa
2. Verificar que la key está activa en https://platform.openai.com/api-keys
3. Regenerar key si es necesario
4. Agregar saldo a la cuenta OpenAI

### P: "Invalid Open Router API Key" en n8n
**R:**
1. Verificar que copió toda la key completa (debe comenzar con `sk-or-`)
2. Verificar que la key está activa en https://openrouter.ai/keys
3. Regenerar key si es necesario
4. Ver `docs/setup-guides/OPENROUTER_SETUP.md` para troubleshooting completo

### P: El agente no entiende mis prompts
**R:** Algunos tips:
- Ser claro: "Crea contacto Ana Gómez con email ana@mail.com"
- Evitar: "Dale de alta a A. G. de A.M." (muy vago)
- El agente entiende variaciones, pero necesita información clara

### P: "Contact ID not found" aunque creé el contacto
**R:** El agente no tiene el ID en memoria:
```
# Opciones:
1. Copiar el ID de Pipedrive y decir: "Agrega nota al contacto ID 123: ..."
2. O ir a Pipedrive y buscar el contacto manualmente
```

---

## 📚 Entendimiento del Sistema

### P: ¿Cómo funciona el flujo conversacional?
**R:** 
```
Usuario → n8n Chat Trigger
       ↓
n8n Chat Memory (guarda contexto)
       ↓
OpenAI o Open Router (interpreta intención)
       ↓
AI Tools (decide qué endpoint llamar)
       ↓
HTTP Nodes (llaman FastAPI)
       ↓
FastAPI (valida y crea en Pipedrive)
       ↓
Respuesta → Usuario
```

### P: ¿Qué hace cada Tool?
**R:**
| Tool | Función |
|------|---------|
| **create_contact** | Crea nuevo contacto con name, email, phone |
| **add_note** | Agrega nota a contacto existente |
| **update_contact** | Actualiza campos (phone, status, etc) |

### P: ¿Qué es Correlation ID?
**R:** Un ID único (UUID) para cada operación. Útil para debugging:
- Ves el ID en logs de FastAPI
- Helps rastrear una operación de principio a fin
- Ejemplo: `correlation_id: 550e8400-e29b-41d4-a716-446655440000`

### P: ¿El sistema guarda datos?
**R:** 
- Logs de operaciones: NO (se pierden al reiniciar)
- Contactos en Pipedrive: SÍ (permanentes)
- Historia de chat en n8n: SÍ (mientras se ejecute)

---

## 🚀 Deployment

### P: ¿Cómo despliego en producción?
**R:** 3 opciones fáciles:
1. **Railway.app** - Click y deploy (recomendado)
2. **Heroku** - Con Heroku CLI
3. **Docker en VPS** - Control total

Ver `docs/deployment/DEPLOYMENT.md` para detalles.

### P: ¿Puedo exponer el chat n8n públicamente?
**R:** Sí, n8n genera una URL pública:
1. En nodo Chat Trigger
2. Copiar URL generada
3. Compartir con usuarios

Importante: Asegurar credenciales en variables de entorno.

### P: ¿Qué es mejor: Cloud Run, Railway o Heroku?
**R:** 
| Opción | Ventaja |
|--------|---------|
| **Railway** | ⭐⭐⭐⭐⭐ Más fácil, buen soporte |
| **Heroku** | ⭐⭐⭐⭐ Muy confiable, gratis con límites |
| **Cloud Run** | ⭐⭐⭐⭐⭐ Más barato si hay bajo uso |

---

## 🔐 Seguridad

### P: ¿Es seguro guardar credenciales en .env?
**R:** 
- ✅ .env en LOCAL es fine
- ❌ NUNCA versionar .env con credenciales reales
- ✅ En producción: usar secrets manager (Railways, Heroku secrets, etc)

### P: ¿Qué validaciones hay?
**R:**
- Email: Validado con Pydantic
- Teléfono: Aceptado como string (flexible)
- Nombre: Mínimo 2 caracteres
- Duplicados: Detectados por email

### P: ¿Puedo usar mis propias credenciales de Pipedrive?
**R:** Sí, completamente:
1. Crear cuenta en Pipedrive
2. Obtener API key
3. Poner en backend/.env
4. Los contactos se crean en TU Pipedrive

---

## 🧪 Testing

### P: ¿Cómo pruebo sin usar Pipedrive real?
**R:** El sistema tiene modo Mock:
- Si `PIPEDRIVE_API_KEY` NO está en .env
- El sistema simula respuestas
- Útil para testing sin credenciales

### P: ¿Dónde veo los logs?
**R:**
- **FastAPI logs**: Terminal donde ejecutas `python main.py`
- **n8n logs**: Execution History en el flujo
- **Ambos**: Guardan Correlation IDs para rastrear

---

## 📈 Performance y Escalabilidad

### P: ¿Cuántas peticiones por segundo puede manejar?
**R:** Localmente: ~100 requests/sec. Depende de:
- Conectividad a Pipedrive
- Rate limits de Pipedrive
- Poder de computadora

### P: ¿Hay límites de Pipedrive?
**R:** Plan gratuito:
- 500 contactos
- Sin límite de APIs calls
- Recomendado: Verificar en https://www.pipedrive.com/pricing

### P: ¿Qué pasa si falla Pipedrive?
**R:** FastAPI retorna error 502:
```json
{
  "detail": "Error comunicándose con Pipedrive"
}
```
n8n muestra el error en el chat.

---

## 👥 Equipo y Contribuciones

### P: ¿Puedo modificar el código?
**R:** Completamente libre:
- Fork el repositorio
- Modifica lo que necesites
- Haz un PR si quieres contribuir

### P: ¿Cómo agrego un nuevo endpoint?
**R:**
```python
# En backend/main.py
@app.post("/crm/custom")
def custom_endpoint(req: CustomRequest):
    # Tu lógica aquí
    return {"success": True}

# Luego en n8n:
# - Crear nuevo Tool
# - Crear nuevo HTTP Node
# - Conectar al agente
```

---

## 📞 Contacto

### P: ¿A quién le reporto un bug?
**R:** 
1. Verificar en `docs/testing-validation/TESTING.md` si está documentado
2. Abrir un Issue en GitHub
3. Incluir: logs, pasos para reproducir, ambiente

### P: ¿Hay soporte técnico?
**R:** No oficial, pero:
- `docs/getting-started/README.md` tiene guías
- `docs/testing-validation/TESTING.md` tiene soluciones
- Este FAQ cubre lo común
- Documentación oficial: n8n.io, fastapi.io

---

## 🎓 Aprendizaje

### P: ¿Cómo aprendo más de n8n?
**R:** 
- Oficial: https://docs.n8n.io
- Youtube: n8n tutorials
- Communidad: https://community.n8n.io

### P: ¿Cómo aprendo más de FastAPI?
**R:**
- Oficial: https://fastapi.tiangolo.com
- Interactive: https://realpython.com/fastapi/
- Youtube: FastAPI tutorials

### P: ¿Cómo aprendo más de Pipedrive API?
**R:**
- Oficial: https://developers.pipedrive.com/docs/api/v1/
- Sandbox: https://app.pipedrive.com (hay API tester)

### P: ¿Cómo aprendo más de Open Router?
**R:**
- Oficial: https://openrouter.ai/docs
- Pricing: https://openrouter.ai/pricing
- Models: https://openrouter.ai/docs/models
- Setup: Ver `docs/setup-guides/OPENROUTER_SETUP.md`

---

## ❓ ¿No encuentras tu pregunta?

Abrir un **Issue en GitHub** con:
1. Descripción clara del problema
2. Pasos para reproducir
3. Sistema operativo y versiones
4. Logs si es relevante

---

**Última actualización:** 2025-12-15

Para guías completas, ver `docs/` con las siguientes carpetas:
- `docs/getting-started/` - Para empezar
- `docs/setup-guides/` - Setup detallado
- `docs/testing-validation/` - Testing
- `docs/deployment/` - Deployment
- `docs/reference/` - Referencia rápida
