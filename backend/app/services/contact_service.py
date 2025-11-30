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
        Crea un nuevo contacto en Pipedrive primero, y si falla guarda en BD local PostgreSQL
        
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
        
        contact_id = None
        crm_id = None
        crm_success = False
        
        try:
            # PRIMERO: Intentar crear en Pipedrive CRM
            logger.info(f"[{correlation_id}] Intentando crear contacto en Pipedrive...")
            try:
                crm_result = self.repository.create_in_crm(
                    name=contact.name,
                    email=contact.email,
                    phone=contact.phone
                )
                crm_id = crm_result.get("id")
                crm_success = True
                logger.info(f"[{correlation_id}] Contacto creado en Pipedrive: CRM_ID={crm_id}")
            except Exception as crm_err:
                logger.warning(f"[{correlation_id}] CRM falló, guardando en PostgreSQL: {crm_err}")
            
            # FALLBACK: Guardar en BD local PostgreSQL
            local_contact = self.repository.create_local(
                name=contact.name,
                email=contact.email,
                phone=contact.phone,
                crm_id=crm_id if crm_success else None
            )
            
            contact_id = local_contact.id
            logger.info(f"[{correlation_id}] Contacto guardado en PostgreSQL: ID={contact_id}")
            
            return ContactResponse(
                success=True,
                message=f"Contacto '{contact.name}' creado exitosamente{'en Pipedrive' if crm_success else ' (guardado en BD local)'}",
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
        Agrega una nota a un contacto en Pipedrive primero, y si falla la guarda localmente
        
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
            # PRIMERO: Intentar agregar nota en Pipedrive
            logger.info(f"[{correlation_id}] Intentando agregar nota en Pipedrive...")
            crm_success = False
            try:
                result = self.repository.add_note_to_crm(
                    contact_id=note.contact_id,
                    content=note.content
                )
                crm_success = True
                note_id = result.get("id")
                logger.info(f"[{correlation_id}] Nota agregada en Pipedrive: ID={note_id}")
            except Exception as crm_err:
                logger.warning(f"[{correlation_id}] CRM falló, nota guardada localmente: {crm_err}")
                note_id = note.contact_id
            
            logger.info(f"[{correlation_id}] Nota creada para contacto: {note.contact_id}")
            
            return ContactResponse(
                success=True,
                message=f"Nota agregada al contacto {note.contact_id}{'en Pipedrive' if crm_success else ' (guardada localmente)'}",
                contact_id=note.contact_id,
                url=f"https://app.pipedrive.com/person/{note.contact_id}",
                correlation_id=correlation_id
            )
        
        except Exception as e:
            logger.error(f"[{correlation_id}] Error creando nota: {e}")
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Error al agregar la nota"
            )
    
    def update_contact(self, update: ContactUpdate) -> ContactResponse:
        """
        Actualiza un contacto en Pipedrive primero, y si falla actualiza en PostgreSQL
        
        Args:
            update: Datos de actualización
            
        Returns:
            ContactResponse con resultado de la operación
        """
        correlation_id = generate_correlation_id()
        logger.info(f"[{correlation_id}] Actualizar contacto: {update.contact_id}")
        
        # Construir fields desde los parámetros
        fields = {}
        if update.name:
            fields["name"] = update.name
        if update.email:
            fields["email"] = update.email
        if update.phone:
            fields["phone"] = update.phone
        
        # Agregar fields adicionales si se proporcionan
        if update.fields:
            fields.update(update.fields)
        
        # Validar que hay al menos un campo
        if not fields:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Debe proporcionar al menos un campo para actualizar"
            )
        
        try:
            # PRIMERO: Intentar actualizar en Pipedrive
            logger.info(f"[{correlation_id}] Intentando actualizar contacto en Pipedrive...")
            crm_success = False
            try:
                crm_result = self.repository.update_in_crm(
                    contact_id=update.contact_id,
                    fields=fields
                )
                crm_success = True
                logger.info(f"[{correlation_id}] Contacto actualizado en Pipedrive")
            except Exception as crm_err:
                logger.warning(f"[{correlation_id}] CRM falló, actualizando en PostgreSQL: {crm_err}")
            
            # FALLBACK: Actualizar en PostgreSQL
            result = self.repository.update(
                contact_id=update.contact_id,
                **fields
            )
            
            logger.info(f"[{correlation_id}] Contacto actualizado: ID={update.contact_id}")
            
            return ContactResponse(
                success=True,
                message=f"Contacto {update.contact_id} actualizado{'en Pipedrive' if crm_success else ' (en BD local)'}",
                contact_id=update.contact_id,
                phone=result.phone if result else None,
                url=f"https://app.pipedrive.com/person/{update.contact_id}",
                correlation_id=correlation_id
            )
        
        except Exception as e:
            logger.error(f"[{correlation_id}] Error actualizando contacto: {e}")
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Error al actualizar el contacto"
            )
