"""
Configuración de base de datos con SQLAlchemy
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import NullPool
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)

# Crear base declarativa para modelos ORM
Base = declarative_base()

# Crear engine de SQLAlchemy
# NullPool: Para desarrollo/testing (crea nueva conexión cada vez)
# En producción usar: QueuePool con pool_size y max_overflow
engine = create_engine(
    settings.DATABASE_URL,
    echo=False,  # Set True para ver SQL queries
    poolclass=NullPool,  # Cambiar a QueuePool en producción
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


async def init_db():
    """
    Inicializa la base de datos creando todas las tablas
    """
    try:
        logger.info("Creando tablas en base de datos...")
        Base.metadata.create_all(bind=engine)
        logger.info("Base de datos inicializada correctamente")
    except Exception as e:
        logger.error(f"Error inicializando base de datos: {e}")
        raise


async def close_db():
    """
    Cierra la conexión a la base de datos
    """
    try:
        logger.info("Cerrando conexión a base de datos...")
        engine.dispose()
        logger.info("Conexión cerrada")
    except Exception as e:
        logger.error(f"Error cerrando conexión: {e}")
