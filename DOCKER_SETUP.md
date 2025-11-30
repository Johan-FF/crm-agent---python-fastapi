# 🐳 Configuración de Docker - Guía de Solución

## Problema: Docker Desktop no está corriendo

**Error encontrado:**
```
error during connect: Head "http://%2F%2F.%2Fpipe%2FdockerDesktopLinuxEngine/_ping": 
open //./pipe/dockerDesktopLinuxEngine: The system cannot find the file specified.
```

**Causa:** Docker Desktop no está iniciado.

---

## ✅ Solución

### Opción 1: Iniciar Docker Desktop Manualmente (Windows)

1. **Presiona `Windows + R`** para abrir el diálogo de ejecución
2. **Escribe:** `Docker Desktop` o ve a `C:\Program Files\Docker\Docker\Docker Desktop.exe`
3. **Presiona Enter** para iniciar Docker Desktop
4. **Espera 30-60 segundos** hasta que aparezca el icono en la bandeja del sistema

### Opción 2: Verificar que Docker Desktop está instalado

```powershell
# Verificar que Docker está instalado
docker --version
# Debería mostrar: Docker version 28.0.4, build b8034c0

# Una vez Docker Desktop esté corriendo:
docker ps
# Debería mostrar una lista de contenedores (vacía si es la primera vez)
```

### Opción 3: Verificar si necesitas Docker Desktop

En Windows, hay dos formas de correr Docker:
- **Docker Desktop** (UI gráfica + daemon) - ✅ Recomendado
- **WSL 2 + Docker Engine** (solo CLI)

Para este proyecto necesitas Docker Desktop corriendo.

---

## 🔍 Verificar que Docker está funcionando

Una vez iniciado Docker Desktop, ejecuta:

```powershell
cd C:\Users\PC_Evalua1\Documents\p2\verticcal-crm-agent

# Verificar Docker
docker --version
docker ps

# Verificar Docker Compose
docker compose version

# Si todo está bien, deberías ver salida sin errores
```

---

## 🚀 Una vez Docker Desktop esté corriendo

```powershell
# 1. Build de la imagen (sin cache)
docker compose build --no-cache

# 2. Iniciar los servicios
docker compose up

# 3. En otra terminal, probar la API
curl http://localhost:8000/contact/health
```

---

## 🆘 Si Docker Desktop sigue sin funcionar

### Opción A: Reiniciar Windows
```powershell
Restart-Computer
# Luego iniciar Docker Desktop nuevamente
```

### Opción B: Desinstalar y reinstalar Docker Desktop
1. Desinstala Docker Desktop desde "Programas y características"
2. Descarga la última versión desde: https://www.docker.com/products/docker-desktop
3. Instala nuevamente
4. Reinicia Windows

### Opción C: Usar WSL 2 Backend
Si tienes WSL 2 instalado:
1. Abre Docker Desktop
2. Settings → Resources → WSL integration
3. Habilita WSL integration
4. Reinicia Docker Desktop

---

## ✅ Checklist después de iniciar Docker

- [ ] Docker Desktop visible en bandeja del sistema (icono)
- [ ] `docker --version` muestra versión
- [ ] `docker ps` no genera error
- [ ] `docker compose version` muestra versión
- [ ] Puedes correr: `docker compose up`

---

## 📝 Warnings ignorables

Estos warnings son normales y no afectan:

```
time="2025-11-30T12:39:48-05:00" level=warning msg="The \"PIPEDRIVE_API_KEY\" variable is not set. Defaulting to a blank string."
→ Normal: PIPEDRIVE_API_KEY es opcional

time="2025-11-30T12:39:48-05:00" level=warning msg="the attribute `version` is obsolete"
→ Puedes quitar la línea `version: '3.8'` de docker-compose.yml si lo deseas
```

---

## 🎯 Próximo Paso

Una vez Docker Desktop esté corriendo:

```bash
cd verticcal-crm-agent
docker compose up
```

Las tablas se crean automáticamente. ✅
