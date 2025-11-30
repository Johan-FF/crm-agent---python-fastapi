"""
Inicialización de base de datos con SQLAlchemy
"""
import logging
from app.db.base import init_db, close_db

logger = logging.getLogger(__name__)


# Los imports se hacen en base.py
# Este módulo exporta las funciones para usar en la app
