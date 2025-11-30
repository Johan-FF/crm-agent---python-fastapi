"""
Dependencias y middleware para FastAPI
"""
from fastapi import Request
from app.core.config import settings
from app.core.security import generate_correlation_id
import logging

logger = logging.getLogger(__name__)


async def add_correlation_id(request: Request, call_next):
    """
    Middleware para agregar correlation_id a todos los requests
    """
    correlation_id = generate_correlation_id()
    request.state.correlation_id = correlation_id
    response = await call_next(request)
    response.headers["X-Correlation-ID"] = correlation_id
    return response


def get_settings():
    """Retorna la instancia de configuración"""
    return settings
