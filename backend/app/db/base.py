"""
Configuración de base de datos
"""
from app.core.config import settings


# SQLAlchemy Database URL (para expansión futura)
DATABASE_URL = settings.DATABASE_URL

# Conexión simple para demostración
# En producción, usar SQLAlchemy, Tortoise-ORM, etc.
class DatabaseConnection:
    """
    Clase base para gestión de conexiones a base de datos
    Placeholder para implementación futura
    """
    
    def __init__(self, database_url: str):
        self.database_url = database_url
    
    async def connect(self):
        """Conectar a la base de datos"""
        pass
    
    async def disconnect(self):
        """Desconectar de la base de datos"""
        pass
