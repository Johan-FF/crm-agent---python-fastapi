"""
Service para contactos (Lógica de negocio)
"""
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
import logging

from app.repositories.contact_repository import ContactRepository
from app.schemas.contact import ContactCreate, ContactUpdate, ContactResponse, NoteCreate
from app.core.security import generate_correlation_id
from fastapi import HTTPException, status

logger = logging.getLogger(__name__)


class ContactService:
    """
    Servicio de contactos
    Contiene la lógica de negocio y validaciones
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.repository = ContactRepository(db)
    
    def create_contact(self, contact: ContactCreate) -> ContactResponse:
        """
        Crea un nuevo contacto en BD local y sincroniza con Pipedrive si está disponible
        
        Args:
            contact: Datos del contacto a crear
            
        Returns:
            ContactResponse con resultado de la operación
        """
        correlation_id = generate_correlation_id()
        logger.info(f"[{correlation_id}] Crear contacto: {contact.name}")
        
        # Validar nombre
        if not contact.name or len(contact.name.strip()) < 2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre debe tener al menos 2 caracteres"
            )
        
        # Verificar duplicados por email en BD local
        if contact.email:
            existing = self.repository.get_by_email(contact.email)
            if existing:
                logger.warning(f"[{correlation_id}] Email duplicado: {contact.email}")
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Ya existe un contacto con email {contact.email}. ID: {existing.id}"
                )
        
        try:
            # Crear en BD local
            local_contact = self.repository.create_local(
                name=contact.name,
                email=contact.email,
                phone=contact.phone
            )
            
            contact_id = local_contact.id
            crm_id = None
            
            # Intentar sincronizar con Pipedrive si hay credenciales
            try:
                crm_result = self.repository.create_in_crm(
                    name=contact.name,
                    email=contact.email,
                    phone=contact.phone
                )
                crm_id = crm_result.get("id")
                
                # Actualizar contact con crm_id
                self.repository.update(contact_id, crm_id=crm_id)
                logger.info(f"[{correlation_id}] Contacto sincronizado con Pipedrive: CRM_ID={crm_id}")
            except Exception as crm_err:
                logger.warning(f"[{correlation_id}] No se sincronizó con Pipedrive: {crm_err}")
            
            logger.info(f"[{correlation_id}] Contacto creado: ID={contact_id}")
            
            return ContactResponse(
                success=True,
                message=f"Contacto '{contact.name}' creado exitosamente",
                contact_id=contact_id,
                crm_id=crm_id,
                url=f"https://app.pipedrive.com/person/{crm_id}" if crm_id else None,
                correlation_id=correlation_id
            )
        
        except Exception as e:
            logger.error(f"[{correlation_id}] Error creando contacto: {e}")
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=str(e)
            )
    
    def add_note_to_contact(self, note: NoteCreate) -> ContactResponse:
        """
        Agrega una nota a un contacto
        
        Args:
            note: Datos de la nota
            
        Returns:
            ContactResponse con resultado de la operación
        """
        correlation_id = generate_correlation_id()
        logger.info(f"[{correlation_id}] Crear nota para contacto: {note.contact_id}")
        
        # Validar contenido
        if not note.content or len(note.content.strip()) < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El contenido de la nota no puede estar vacío"
            )
        
        try:
            # Crear nota en repositorio
            result = self.repository.add_note(
                contact_id=note.contact_id,
                content=note.content
            )
            
            note_id = result.get("id")
            logger.info(f"[{correlation_id}] Nota creada: ID={note_id}")
            
            return ContactResponse(
                success=True,
                message=f"Nota agregada al contacto {note.contact_id}",
                contact_id=note.contact_id,
                url=f"https://app.pipedrive.com/person/{note.contact_id}",
                correlation_id=correlation_id
            )
        
        except Exception as e:
            logger.error(f"[{correlation_id}] Error creando nota: {e}")
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Error comunicándose con el CRM"
            )
    
    def update_contact(self, update: ContactUpdate) -> ContactResponse:
        """
        Actualiza un contacto
        
        Args:
            update: Datos de actualización
            
        Returns:
            ContactResponse con resultado de la operación
        """
        correlation_id = generate_correlation_id()
        logger.info(f"[{correlation_id}] Actualizar contacto: {update.contact_id}")
        
        # Validar campos
        if not update.fields:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Debe proporcionar al menos un campo para actualizar"
            )
        
        try:
            # Actualizar en repositorio
            result = self.repository.update(
                contact_id=update.contact_id,
                fields=update.fields
            )
            
            logger.info(f"[{correlation_id}] Contacto actualizado: ID={update.contact_id}")
            
            return ContactResponse(
                success=True,
                message=f"Contacto {update.contact_id} actualizado",
                contact_id=update.contact_id,
                url=f"https://app.pipedrive.com/person/{update.contact_id}",
                correlation_id=correlation_id
            )
        
        except Exception as e:
            logger.error(f"[{correlation_id}] Error actualizando contacto: {e}")
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Error comunicándose con el CRM"
            )
