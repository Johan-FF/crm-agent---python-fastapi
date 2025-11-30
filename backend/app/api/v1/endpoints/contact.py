"""
Endpoints de contactos (API v1)
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import logging
from datetime import datetime

from app.schemas.contact import (
    ContactCreate, ContactUpdate, ContactResponse, 
    NoteCreate, HealthResponse
)
from app.services.contact_service import ContactService
from app.core.dependencies import get_settings
from app.db.session import get_db
from app.core.config import Settings

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/contact", tags=["contacts"])


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
async def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo contacto en BD local y sincroniza con Pipedrive
    
    Args:
        contact: Datos del contacto (name, email, phone)
        db: Dependencia de sesión de base de datos
    
    Returns:
        ContactResponse con resultado de la operación
    
    Raises:
        400: Validación fallida
        409: Contacto duplicado (email existe)
        502: Error comunicándose con el CRM
    """
    logger.info(f"POST /contact - Creando contacto: {contact.name}")
    service = ContactService(db)
    return service.create_contact(contact)


@router.post("/note", response_model=ContactResponse)
async def add_note(note: NoteCreate, db: Session = Depends(get_db)):
    """
    Agrega una nota a un contacto existente
    
    Args:
        note: Datos de la nota (contact_id, content)
        db: Dependencia de sesión de base de datos
    
    Returns:
        ContactResponse con resultado de la operación
    
    Raises:
        400: Validación fallida
        502: Error comunicándose con el CRM
    """
    logger.info(f"POST /contact/note - Agregando nota a contacto: {note.contact_id}")
    service = ContactService(db)
    return service.add_note_to_contact(note)


@router.patch("", response_model=ContactResponse)
async def update_contact(update: ContactUpdate, db: Session = Depends(get_db)):
    """
    Actualiza un contacto existente
    
    Args:
        update: Datos de actualización (contact_id, fields)
        db: Dependencia de sesión de base de datos
    
    Returns:
        ContactResponse con resultado de la operación
    
    Raises:
        400: Validación fallida
        502: Error comunicándose con el CRM
    """
    logger.info(f"PATCH /contact - Actualizando contacto: {update.contact_id}")
    service = ContactService(db)
    return service.update_contact(update)
