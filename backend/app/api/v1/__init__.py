"""
Router para API v1
"""
from fastapi import APIRouter

from app.api.v1.endpoints import contact

# Crear router principal de v1
router = APIRouter(prefix="/api/v1")

# Incluir endpoints de contactos
router.include_router(contact.router)
