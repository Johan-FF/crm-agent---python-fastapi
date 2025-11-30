# 📚 Índice de Documentación - Verticcal CRM Agent

> Navegación rápida a todos los documentos del proyecto

---

## 🚀 Empezar Aquí

1. **[docs/getting-started/QUICKSTART.md](docs/getting-started/QUICKSTART.md)** ⭐ **LEER PRIMERO** (5 min)
   - Setup en 10 pasos simples
   - Para quienes quieren ir rápido
   
2. **[docs/getting-started/README.md](docs/getting-started/README.md)** - Guía Principal Completa
   - Descripción general
   - Arquitectura con diagrama
   - Setup local y Docker
   - Endpoints REST
   - Troubleshooting

---

## 📖 Documentación Específica

### Setup e Instalación
- **[docs/getting-started/QUICKSTART.md](docs/getting-started/QUICKSTART.md)** - Fast track (5 min)
- **[docs/setup-guides/N8N_SETUP_GUIDE.md](docs/setup-guides/N8N_SETUP_GUIDE.md)** - Configurar n8n específicamente
- **[docs/getting-started/README.md](docs/getting-started/README.md)** - Guía completa paso a paso

### Setup de Open Router
- **[docs/setup-guides/OPENROUTER_SETUP.md](docs/setup-guides/OPENROUTER_SETUP.md)** - Guía completa (recomendado)
- **[docs/setup-guides/OPENROUTER_MIGRATION.md](docs/setup-guides/OPENROUTER_MIGRATION.md)** - Cambio de OpenAI
- **[docs/getting-started/OPENROUTER_README.md](docs/getting-started/OPENROUTER_README.md)** - Resumen ejecutivo

### Testing y Validación
- **[docs/testing-validation/TESTING.md](docs/testing-validation/TESTING.md)** - 20+ casos de prueba detallados
  - Crear contacto (5 variantes)
  - Agregar nota (5 variantes)
  - Actualizar campo (5 variantes)
  - Flujo conversacional completo
  - Tests de endpoints manuales

### Deployment y Producción
- **[docs/deployment/DEPLOYMENT.md](docs/deployment/DEPLOYMENT.md)** - Guías de despliegue
  - Railway (recomendado - más fácil)
  - Heroku
  - Google Cloud Run
  - VPS + Docker Compose
  - Security checklist
  - Scaling considerations

### Preguntas Comunes
- **[docs/reference/FAQ.md](docs/reference/FAQ.md)** - Preguntas frecuentes responden:
  - Setup y configuración
  - Costes (OpenAI vs Open Router)
  - Problemas técnicos
  - Cómo funciona el sistema
  - Deployment
  - Seguridad
  - Y más...

### Resumen Ejecutivo
- **[docs/getting-started/EXECUTIVE_SUMMARY.md](docs/getting-started/EXECUTIVE_SUMMARY.md)** - Overview ejecutivo
  - Lo que se entregó
  - Features implementadas
  - Stack técnico
  - Decisiones de diseño
  - Checklist de entrega

---

## 🗂️ Estructura del Código

```
verticcal-crm-agent/
│
├── 📁 docs/                           # 📚 Documentación organizada por tema
│   ├── getting-started/
│   │   ├── README.md                  # Guía principal
│   │   ├── QUICKSTART.md              # Setup rápido (5 min) ⭐ LEER PRIMERO
│   │   ├── EXECUTIVE_SUMMARY.md       # Resumen ejecutivo
│   │   └── OPENROUTER_README.md       # Info sobre Open Router
│   │
│   ├── setup-guides/
│   │   ├── N8N_SETUP_GUIDE.md         # Configurar n8n
│   │   ├── OPENROUTER_SETUP.md        # Setup completo Open Router ⭐
│   │   └── OPENROUTER_MIGRATION.md    # Migración OpenAI → Open Router
│   │
│   ├── testing-validation/
│   │   └── TESTING.md                 # 20+ casos de prueba detallados
│   │
│   ├── deployment/
│   │   └── DEPLOYMENT.md              # Railway, Heroku, GCP, VPS
│   │
│   ├── architecture/                  # Diagramas y diseño técnico (placeholder)
│   │
│   └── reference/
│       ├── FAQ.md                     # Preguntas frecuentes
│       └── VIDEO_GUIDE.md             # Cómo grabar demo (si existe)
│
├── 📄 INDEX.md                        # Este archivo - Índice de documentación
│
├── 🔧 CONFIGURACIÓN
│   ├── docker-compose.yml             # Orquestar servicios
│   ├── .env.example                   # Variables de entorno
│   └── .gitignore                     # Git configuration
│
├── 📦 BACKEND (FastAPI)
│   └── backend/
│       ├── main.py                    # Aplicación principal
│       ├── requirements.txt           # Dependencias Python
│       ├── Dockerfile                 # Imagen Docker
│       └── .env.example               # Variables backend
│
├── 🤖 FLUJO N8N
│   └── n8n-workflows/
│       ├── verticcal-crm-agent-workflow.json                   # OpenAI original
│       └── verticcal-crm-agent-workflow-openrouter.json        # Open Router (nuevo)
│
└── 🛠️ UTILIDADES
    ├── validate_setup.py              # Validar installation
    ├── setup.sh                       # Setup automático (Linux/Mac)
    └── setup.ps1                      # Setup automático (Windows)
```

---

## 🎯 Qué Leer Según tu Rol

### 👨‍💼 Manager / Stakeholder
1. **[docs/getting-started/EXECUTIVE_SUMMARY.md](docs/getting-started/EXECUTIVE_SUMMARY.md)** - 5 min
2. **[docs/getting-started/README.md → Arquitectura](docs/getting-started/README.md)** - Entender flujo
3. Video demo (si existe) - Ver funcionando

### 👨‍💻 Developer (Setup Local)
1. **[docs/getting-started/QUICKSTART.md](docs/getting-started/QUICKSTART.md)** - 5 min ⭐
2. **[docs/getting-started/README.md](docs/getting-started/README.md)** - 15 min
3. **[docs/testing-validation/TESTING.md](docs/testing-validation/TESTING.md)** - Validar todo funciona
4. **Código en `backend/main.py`** - Entender lógica

### 🔧 DevOps / Deploy
1. **[docs/deployment/DEPLOYMENT.md](docs/deployment/DEPLOYMENT.md)** - 20 min
2. **[docs/getting-started/README.md → Docker](docs/getting-started/README.md)** - Entender setup
3. **docker-compose.yml** - Configurar según necesidad

### 💰 Quiero usar Open Router (más barato)
1. **[docs/setup-guides/OPENROUTER_SETUP.md](docs/setup-guides/OPENROUTER_SETUP.md)** - 10 min ⭐
2. **[docs/setup-guides/OPENROUTER_MIGRATION.md](docs/setup-guides/OPENROUTER_MIGRATION.md)** - Cambio rápido
3. **[docs/reference/FAQ.md → Costes](docs/reference/FAQ.md)** - Ver ahorro

### 🧪 QA / Tester
1. **[docs/testing-validation/TESTING.md](docs/testing-validation/TESTING.md)** - 30 min (léelo todo)
2. **[docs/getting-started/QUICKSTART.md](docs/getting-started/QUICKSTART.md)** - Setup para testing
3. Ejecutar todos los casos uno por uno

### ❓ Necesitas Ayuda
1. **[docs/reference/FAQ.md](docs/reference/FAQ.md)** - Tu pregunta probablemente está ahí
2. **[docs/getting-started/README.md → Troubleshooting](docs/getting-started/README.md)** - Problemas comunes
3. **Revisar logs** en `backend/main.py` output

---

## 📋 Checklist de Lectura

### Lectura Mínima (15 min)
- [ ] `docs/getting-started/QUICKSTART.md`
- [ ] `docs/getting-started/README.md` (Architecture + Setup)

### Lectura Completa (1 hora)
- [ ] `docs/getting-started/QUICKSTART.md`
- [ ] `docs/getting-started/README.md` (todo)
- [ ] `docs/getting-started/EXECUTIVE_SUMMARY.md`
- [ ] `docs/reference/FAQ.md` (secciones relevantes)

### Para Setup con Open Router (30 min)
- [ ] `docs/getting-started/QUICKSTART.md`
- [ ] `docs/setup-guides/OPENROUTER_SETUP.md` ⭐
- [ ] `docs/setup-guides/OPENROUTER_MIGRATION.md`
- [ ] `docs/reference/FAQ.md → Costes`

### Lectura Experta (2+ horas)
- [ ] Todo lo anterior +
- [ ] `docs/testing-validation/TESTING.md` (completo)
- [ ] `docs/deployment/DEPLOYMENT.md` (completo)
- [ ] Código en `backend/main.py`
- [ ] Flujo n8n en JSON

---

## 🚀 Próximos Pasos

### Para Empezar Ahora (15 min)
```bash
# 1. Leer docs/getting-started/QUICKSTART.md (5 min)
# 2. Ejecutar setup automático
./setup.ps1          # Windows
./setup.sh           # Mac/Linux

# 3. Configurar .env con Pipedrive API key
# 4. Correr FastAPI y n8n
# 5. Importar flujo en n8n
# 6. Probar los 3 casos en docs/testing-validation/TESTING.md
```

### Para usar Open Router (25 min)
```bash
# 1. Leer docs/setup-guides/OPENROUTER_SETUP.md (10 min)
# 2. Registrarse en https://openrouter.ai (5 min)
# 3. Obtener API key en https://openrouter.ai/keys (1 min)
# 4. Configurar .env con OPEN_ROUTER_API_KEY
# 5. Importar verticcal-crm-agent-workflow-openrouter.json en n8n
# 6. Testear
```

### Para Desplegar (60+ min)
```bash
# 1. Leer docs/deployment/DEPLOYMENT.md (20 min)
# 2. Elegir plataforma (Railway recomendado)
# 3. Seguir pasos específicos (30 min)
# 4. Testear en la nube (10 min)
```

---

## 🔍 Buscar en Documentación

### Por Problema
| Problema | Documento |
|----------|-----------|
| No sé por dónde empezar | `docs/getting-started/QUICKSTART.md` ⭐ |
| FastAPI no inicia | `docs/reference/FAQ.md` → Troubleshooting |
| n8n no conecta | `docs/getting-started/README.md` → Troubleshooting |
| ¿Cómo despliego? | `docs/deployment/DEPLOYMENT.md` |
| ¿Cuánto cuesta? | `docs/reference/FAQ.md` → Costes |
| ¿Es más barato que OpenAI? | `docs/setup-guides/OPENROUTER_SETUP.md` |
| Quiero usar Open Router | `docs/setup-guides/OPENROUTER_SETUP.md` ⭐ |

### Por Tema
| Tema | Documentos |
|------|-----------|
| Setup | `docs/getting-started/QUICKSTART.md`, `docs/getting-started/README.md`, `docs/setup-guides/N8N_SETUP_GUIDE.md` |
| Open Router | `docs/setup-guides/OPENROUTER_SETUP.md`, `docs/setup-guides/OPENROUTER_MIGRATION.md` |
| Testing | `docs/testing-validation/TESTING.md` |
| Deployment | `docs/deployment/DEPLOYMENT.md` |
| Troubleshooting | `docs/getting-started/README.md`, `docs/reference/FAQ.md` |
| Código | `backend/main.py`, `n8n-workflows/workflow.json` |

---

## 📞 Navegación Rápida

- **Quiero empezar → `docs/getting-started/QUICKSTART.md` ⭐**
- **Necesito ayuda → `docs/reference/FAQ.md`**
- **Quiero entender → `docs/getting-started/README.md`**
- **Voy a testear → `docs/testing-validation/TESTING.md`**
- **Voy a desplegar → `docs/deployment/DEPLOYMENT.md`**
- **Quiero ahorrar dinero → `docs/setup-guides/OPENROUTER_SETUP.md` ⭐**

---

## 📊 Estadísticas de Documentación

| Documento | Ubicación | Tiempo Lectura |
|-----------|-----------|----------------|
| QUICKSTART.md | `docs/getting-started/` | 5 min |
| README.md | `docs/getting-started/` | 15 min |
| TESTING.md | `docs/testing-validation/` | 15 min |
| DEPLOYMENT.md | `docs/deployment/` | 12 min |
| FAQ.md | `docs/reference/` | 12 min |
| EXECUTIVE_SUMMARY.md | `docs/getting-started/` | 8 min |
| OPENROUTER_SETUP.md | `docs/setup-guides/` | 10 min |
| **TOTAL** | **docs/** | **1.5+ horas** |

---

## ✅ Validación Completa

Cuando hayas terminado todo, verifica:

- [ ] Leí `docs/getting-started/QUICKSTART.md`
- [ ] Ejecuté setup
- [ ] Configuré `.env`
- [ ] FastAPI corre
- [ ] n8n corre
- [ ] Flujo importado
- [ ] LLM configurado (OpenAI o Open Router)
- [ ] Caso 1 (Create) funciona
- [ ] Caso 2 (Note) funciona
- [ ] Caso 3 (Update) funciona
- [ ] Leí `docs/reference/FAQ.md`
- [ ] Sé cómo hacer deploy
- [ ] Sé cómo cambiar a Open Router (si interesa)

---

**Última actualización:** 2025-12-15

**Versión:** 2.0 - Con Open Router Integration

**Estado:** Ready for Production

**Licencia:** MIT

---

**📌 IMPORTANTE:** Toda la documentación está organizada en la carpeta `docs/` con subcarpetas temáticas. Los archivos antiguos en el root se mantienen por compatibilidad, pero se recomienda usar los de `docs/` que incluyen referencias actualizadas a Open Router.
