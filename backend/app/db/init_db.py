"""
Inicialización de base de datos
"""
import logging

logger = logging.getLogger(__name__)


async def init_db():
    """
    Inicializa la base de datos
    Crea tablas, seedea datos, etc.
    """
    logger.info("Inicializando base de datos...")
    # Implementación futura: crear tablas, indices, etc.
    pass


async def close_db():
    """
    Cierra la conexión a la base de datos
    """
    logger.info("Cerrando conexión a base de datos...")
    pass
