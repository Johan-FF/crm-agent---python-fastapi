# Cambio de OpenAI a Open Router ✅

## Resumen de cambios realizados

### 📋 Archivos actualizados:

1. **`backend/.env.example`**
   - ✅ Agregadas variables para Open Router
   - ✅ Documentación sobre modelos disponibles

2. **`n8n-workflows/ -crm-agent-workflow-openrouter.json`** (NUEVO)
   - ✅ Workflow completo configurado para Open Router
   - ✅ Nodo HTTP Request apuntando a `https://openrouter.ai/api/v1/chat/completions`
   - ✅ Headers necesarios (Authorization, HTTP-Referer, X-Title)
   - ✅ Soporte para cambiar modelo dinámicamente via `$env.OPEN_ROUTER_MODEL`

3. **`README.md`**
   - ✅ Actualizado requisitos previos
   - ✅ Instrucciones de setup para Open Router
   - ✅ Dos opciones: Open Router (recomendado) y OpenAI (alternativa)

4. **`QUICKSTART.md`**
   - ✅ Agregadas instrucciones para obtener API key de Open Router
   - ✅ Actualizado paso 5 con variables para ambos servicios

5. **`docs/setup-guides/OPENROUTER_SETUP.md`** (NUEVO - Guía completa)
   - ✅ Cómo registrarse en Open Router
   - ✅ Cómo obtener API key
   - ✅ Comparación de modelos y precios
   - ✅ Guía de monitoreo de gastos
   - ✅ Troubleshooting completo
   - ✅ Ejemplos de configuración

---

## 🎯 Ventajas del cambio

| Aspecto | OpenAI | Open Router |
|---------|--------|-------------|
| **Precio** | $0.03 / 1K tokens | $0.0005 / 1K tokens (GPT-3.5) |
| **Modelos** | Solo OpenAI | 30+ modelos (GPT-4, Claude, Llama, etc.) |
| **Facilidad** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Fallback** | ❌ No | ✅ Automático si modelo no disponible |
| **Costo estimado (100 llamadas)** | $3-5 | $0.05-0.10 |

---

## 📦 Cómo usar

### Opción 1: Open Router (RECOMENDADO)

1. Registrarse en https://openrouter.ai
2. Obtener API key en https://openrouter.ai/keys
3. Configurar en `backend/.env`:
   ```
   OPEN_ROUTER_API_KEY=sk-or-xxxxx
   OPEN_ROUTER_MODEL=openai/gpt-3.5-turbo
   ```
4. Importar en n8n: ` -crm-agent-workflow-openrouter.json`

### Opción 2: OpenAI (alternativa)

1. Usar API key de OpenAI
2. Configurar en `backend/.env`:
   ```
   OPENAI_API_KEY=sk-xxxxx
   ```
3. Importar en n8n: ` -crm-agent-workflow.json` (original)

---

## 🔄 Migración desde OpenAI

Si ya tenías configurado OpenAI:

1. Registrate en Open Router (5 min)
2. Obtén tu API key (1 min)
3. Actualiza `backend/.env` con `OPEN_ROUTER_API_KEY`
4. Descarga e importa ` -crm-agent-workflow-openrouter.json` en n8n
5. Listo

**No necesitas cambiar nada en FastAPI**, solo cambia el flujo de n8n.

---

## ❓ Preguntas frecuentes

### ¿Puedo seguir usando OpenAI?
✅ Sí, el workflow original sigue disponible. Ambas opciones funcionan.

### ¿Cuál es más barato?
Open Router es 50-60x más barato para GPT-3.5-turbo.
Para GPT-4, es aproximadamente 5x más barato.

### ¿Cuál tiene mejor calidad?
Son equivalentes. Open Router solo actúa como intermediario.

### ¿Cuál debo usar?
**Recomendación**: Open Router para desarrollo y pruebas (muy barato).
Para producción, depende de tus necesidades.

---

## 📚 Documentación completa

Para más información, ver:
- `docs/setup-guides/OPENROUTER_SETUP.md` - Guía paso a paso
- `docs/getting-started/README.md` - Instrucciones de setup
- `docs/getting-started/QUICKSTART.md` - Setup rápido (5 min)

---

## ✅ Próximos pasos

1. Lee `docs/setup-guides/OPENROUTER_SETUP.md`
2. Registrate en https://openrouter.ai
3. Configura tu API key en `backend/.env`
4. Importa ` -crm-agent-workflow-openrouter.json` en n8n
5. Testea los 3 casos de uso

¿Preguntas? Ver `docs/reference/FAQ.md` o `docs/setup-guides/OPENROUTER_SETUP.md`
