"""
Gestión de sesiones de base de datos
"""
from typing import AsyncGenerator
from app.db.base import DatabaseConnection, DATABASE_URL
from app.db.init_db import init_db, close_db

# Instancia de conexión a la base de datos
db = DatabaseConnection(DATABASE_URL)


async def get_db() -> AsyncGenerator:
    """
    Dependencia para inyectar la sesión de base de datos en endpoints
    """
    yield db
