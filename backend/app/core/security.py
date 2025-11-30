"""
Módulo de seguridad y utilidades de autenticación
"""
import uuid
import logging

logger = logging.getLogger(__name__)


def generate_correlation_id() -> str:
    """
    Genera un ID de correlación único para rastrear requests
    
    Returns:
        str: UUID como string
    """
    return str(uuid.uuid4())


def generate_mock_id(seed: str) -> int:
    """
    Genera un ID numérico para modo mock
    
    Args:
        seed: String para generar el hash
        
    Returns:
        int: ID numérico
    """
    return hash(seed) % 100000
