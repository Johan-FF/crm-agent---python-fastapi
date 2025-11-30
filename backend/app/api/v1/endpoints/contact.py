"""
Endpoints de contactos (API v1)
"""
from fastapi import APIRouter, HTTPException, status, Depends
import logging
from datetime import datetime

from app.schemas.contact import (
    ContactCreate, ContactUpdate, ContactResponse, 
    NoteCreate, HealthResponse
)
from app.services.contact_service import ContactService
from app.core.dependencies import get_settings
from app.core.config import Settings

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/contact", tags=["contacts"])

# Instancia del servicio
contact_service = ContactService()


@router.get("/health", response_model=HealthResponse)
async def health_check(settings: Settings = Depends(get_settings)):
    """
    Verifica el estado de la API y disponibilidad del CRM
    
    Returns:
        HealthResponse con estado actual
    """
    logger.info("Health check endpoint")
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow(),
        crm_configured=settings.crm_configured
    )


@router.post("", response_model=ContactResponse)
async def create_contact(contact: ContactCreate):
    """
    Crea un nuevo contacto en el CRM
    
    Args:
        contact: Datos del contacto (name, email, phone)
    
    Returns:
        ContactResponse con resultado de la operación
    
    Raises:
        400: Validación fallida
        409: Contacto duplicado (email existe)
        502: Error comunicándose con el CRM
    """
    logger.info(f"POST /contact - Creando contacto: {contact.name}")
    return contact_service.create_contact(contact)


@router.post("/note", response_model=ContactResponse)
async def add_note(note: NoteCreate):
    """
    Agrega una nota a un contacto existente
    
    Args:
        note: Datos de la nota (contact_id, content)
    
    Returns:
        ContactResponse con resultado de la operación
    
    Raises:
        400: Validación fallida
        502: Error comunicándose con el CRM
    """
    logger.info(f"POST /contact/note - Agregando nota a contacto: {note.contact_id}")
    return contact_service.add_note_to_contact(note)


@router.patch("", response_model=ContactResponse)
async def update_contact(update: ContactUpdate):
    """
    Actualiza un contacto existente
    
    Args:
        update: Datos de actualización (contact_id, fields)
    
    Returns:
        ContactResponse con resultado de la operación
    
    Raises:
        400: Validación fallida
        502: Error comunicándose con el CRM
    """
    logger.info(f"PATCH /contact - Actualizando contacto: {update.contact_id}")
    return contact_service.update_contact(update)
