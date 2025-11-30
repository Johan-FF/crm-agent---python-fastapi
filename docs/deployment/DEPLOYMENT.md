# ☁️ Guía de Despliegue en la Nube

Este documento explica opciones para desplegar Verticcal CRM Agent en producción.

## 🚀 Opción 1: Despliegue con Railway (Recomendado - Más Simple)

Railway es una plataforma que permite desplegar aplicaciones con un solo click.

### Requisitos
- Cuenta en [Railway.app](https://railway.app)
- GitHub (para conectar el repositorio)

### Pasos

1. **Subir el código a GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Verticcal CRM Agent"
   git remote add origin https://github.com/tu-usuario/verticcal-crm-agent.git
   git push -u origin main
   ```

2. **Crear proyecto en Railway**
   - Ir a https://railway.app
   - Click en "New Project"
   - Click en "Deploy from GitHub repo"
   - Seleccionar tu repositorio
   - Railway detectará que es Python

3. **Configurar Variables de Entorno**
   - En Railway, ir a "Variables"
   - Agregar:
     ```
     PIPEDRIVE_API_KEY=your_api_key
     PIPEDRIVE_BASE_URL=https://api.pipedrive.com/v1
     ```

4. **Desplegar**
   - Railway automáticamente inicia el despliegue
   - Esperar a que termine
   - Obtener URL pública (ej: `https://verticcal-crm.railway.app`)

### Usar FastAPI Desplegado con n8n Local
1. En n8n, cambiar URLs HTTP de:
   - `http://localhost:8000` 
   - a `https://verticcal-crm.railway.app`
2. Guardar y testear

---

## 🐳 Opción 2: Despliegue con Docker + Heroku

### Requisitos
- Docker instalado
- Cuenta en [Heroku](https://heroku.com)
- Heroku CLI

### Pasos

1. **Login en Heroku**
   ```bash
   heroku login
   ```

2. **Crear app en Heroku**
   ```bash
   heroku create verticcal-crm-api
   ```

3. **Agregar variables de entorno**
   ```bash
   heroku config:set PIPEDRIVE_API_KEY=your_key
   heroku config:set PIPEDRIVE_BASE_URL=https://api.pipedrive.com/v1
   ```

4. **Desplegar**
   ```bash
   git push heroku main
   ```

5. **Verificar**
   ```bash
   heroku logs --tail
   heroku open
   ```

---

## ☁️ Opción 3: Despliegue con Google Cloud Run

Google Cloud Run permite ejecutar contenedores serverless (pagas por uso).

### Requisitos
- Cuenta Google Cloud
- Docker instalado
- Google Cloud CLI

### Pasos

1. **Autenticar con Google Cloud**
   ```bash
   gcloud auth login
   gcloud config set project your-project-id
   ```

2. **Construir imagen Docker**
   ```bash
   gcloud builds submit --tag gcr.io/your-project/verticcal-crm
   ```

3. **Desplegar en Cloud Run**
   ```bash
   gcloud run deploy verticcal-crm \
     --image gcr.io/your-project/verticcal-crm \
     --platform managed \
     --region us-central1 \
     --set-env-vars PIPEDRIVE_API_KEY=your_key
   ```

4. **Obtener URL**
   - Google Cloud da una URL pública
   - Usar en n8n

---

## 🎯 Opción 4: Despliegue Completo (FastAPI + n8n) con Docker Compose en VPS

Si quieres desplegar todo (FastAPI + n8n) en un servidor VPS propio.

### Requisitos
- VPS (DigitalOcean, Linode, AWS EC2, etc.)
- Docker y Docker Compose instalados
- Dominio (opcional, pero recomendado)

### Pasos

1. **Clonar en el VPS**
   ```bash
   ssh user@your-server.com
   git clone https://github.com/tu-usuario/verticcal-crm-agent.git
   cd verticcal-crm-agent
   ```

2. **Crear .env**
   ```bash
   cp .env.example .env
   # Editar con tu API key
   nano .env
   ```

3. **Usar Docker Compose con Nginx (Reverse Proxy)**
   
   Crear `docker-compose.prod.yml`:
   ```yaml
   version: '3.8'
   
   services:
     fastapi:
       build:
         context: ./backend
         dockerfile: Dockerfile
       environment:
         - PIPEDRIVE_API_KEY=${PIPEDRIVE_API_KEY}
       networks:
         - verticcal-network
       restart: always
     
     n8n:
       image: n8nio/n8n:latest
       environment:
         - N8N_HOST=${DOMAIN}
         - N8N_PORT=80
         - WEBHOOK_TUNNEL_URL=https://${DOMAIN}/
       volumes:
         - n8n_storage:/home/node/.n8n
       networks:
         - verticcal-network
       restart: always
     
     nginx:
       image: nginx:latest
       ports:
         - "80:80"
         - "443:443"
       volumes:
         - ./nginx.conf:/etc/nginx/nginx.conf:ro
         - ./certs:/etc/nginx/certs:ro
       networks:
         - verticcal-network
       depends_on:
         - fastapi
         - n8n
       restart: always
   
   networks:
     verticcal-network:
   
   volumes:
     n8n_storage:
   ```

4. **Levantar servicios**
   ```bash
   DOMAIN=your-domain.com docker-compose -f docker-compose.prod.yml up -d
   ```

5. **Configurar SSL con Certbot** (opcional pero recomendado)
   ```bash
   sudo certbot certonly --standalone -d your-domain.com
   ```

---

## 📋 Comparativa de Opciones

| Opción | Coste | Facilidad | Escalabilidad | Recomendado |
|--------|-------|-----------|---------------|------------|
| Railway | ~$5/mes | ⭐⭐⭐⭐⭐ | Media | ✅ Para empezar |
| Heroku | ~$7/mes | ⭐⭐⭐⭐ | Media | ✅ Muy buena |
| Cloud Run | Pago por uso | ⭐⭐⭐ | Alta | ✅ Para escala |
| VPS + Compose | ~$5-10/mes | ⭐⭐⭐ | Según VPS | ✅ Control total |

---

## 🔐 Seguridad en Producción

**Antes de desplegar:**

1. **Variables de Entorno**
   - Nunca versionar `.env` con credenciales reales
   - Usar secrets management de la plataforma

2. **CORS**
   - Cambiar `allow_origins=["*"]` a dominios específicos
   - En `backend/main.py`:
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["https://tu-dominio.com", "https://n8n.tu-dominio.com"],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

3. **Rate Limiting**
   - Agregar rate limiting para evitar abuso
   - En FastAPI:
   ```python
   from slowapi import Limiter
   from slowapi.util import get_remote_address
   
   limiter = Limiter(key_func=get_remote_address)
   
   @app.post("/crm/contact")
   @limiter.limit("10/minute")
   async def create_contact(...):
       ...
   ```

4. **Logging y Monitoring**
   - Configurar alertas para errores
   - Usar servicios como Sentry, DataDog, etc.

5. **Validación de Input**
   - Ya está implementado con Pydantic
   - Asegurar que FastAPI valida todos los inputs

---

## 📈 Scaling

Si el sistema crece:

1. **Separar servicios**
   - FastAPI en su propio cluster
   - n8n en cluster separado

2. **Database**
   - Agregar PostgreSQL para persistencia
   - Guardar logs de todas las operaciones

3. **Message Queue**
   - Usar Redis para manejo asincrónico
   - Colas de trabajo para operaciones largas

4. **CDN**
   - Para archivos estáticos
   - Cloudflare, AWS CloudFront, etc.

---

## 🔗 Referencias

- [Railway Docs](https://docs.railway.app)
- [Heroku Docs](https://devcenter.heroku.com)
- [Google Cloud Run](https://cloud.google.com/run/docs)
- [Docker Compose Production](https://docs.docker.com/compose/production)
