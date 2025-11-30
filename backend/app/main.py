"""
Aplicación FastAPI principal
Punto de entrada para la API del backend
"""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.dependencies import add_correlation_id
from app.api.v1 import router as v1_router
from app.db.base import init_db, close_db

# Configurar logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# Eventos de ciclo de vida
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Maneja el ciclo de vida de la aplicación
    - Startup: Inicializa la base de datos PostgreSQL
    - Shutdown: Cierra las conexiones
    """
    # Startup
    logger.info("Iniciando aplicación...")
    logger.info(f"CRM configurado: {settings.crm_configured}")
    logger.info(f"Modo mock: {settings.is_mock_mode}")
    logger.info("Inicializando base de datos PostgreSQL...")
    
    try:
        # Inicializar BD (crea tablas si no existen)
        init_db()
        logger.info("✓ Base de datos inicializada correctamente")
    except Exception as e:
        logger.error(f"✗ Error al inicializar base de datos: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Cerrando aplicación...")
    try:
        close_db()
        logger.info("✓ Conexiones de base de datos cerradas")
    except Exception as e:
        logger.error(f"✗ Error al cerrar base de datos: {e}")


# Crear aplicación FastAPI
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    lifespan=lifespan
)

# Agregar middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

# Agregar middleware de correlation ID
app.middleware("http")(add_correlation_id)


# Incluir routers
app.include_router(v1_router)


# Endpoint raíz
@app.get("/")
async def root():
    """
    Endpoint raíz - Bienvenida a la API
    """
    return {
        "message": "CRM Agent API",
        "version": settings.API_VERSION,
        "docs": "/docs",
        "api": "/api/v1",
        "database": "PostgreSQL"
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
