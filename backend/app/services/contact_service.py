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
    
    def search_contact(self, query: str) -> Dict[str, Any]:
        """
        Busca un contacto por nombre, email o teléfono
        Primero en Pipedrive, luego en BD local
        
        Args:
            query: String de búsqueda
            
        Returns:
            Dict con datos del contacto o 404
        """
        correlation_id = generate_correlation_id()
        logger.info(f"[{correlation_id}] Buscar contacto: {query}")
        
        # PRIMERO: Intentar buscar en Pipedrive CRM
        try:
            # Buscar por email en CRM
            crm_contact = self.repository.get_by_email_from_crm(query)
            
            # Si no se encuentra, buscar por nombre
            if not crm_contact:
                crm_contact = self.repository.get_by_name_from_crm(query)
            
            if crm_contact:
                logger.info(f"[{correlation_id}] Contacto encontrado en Pipedrive: {crm_contact.get('id')}")
                
                # Buscar en BD local si existe con ese crm_id
                local_contact = self.repository.get_by_crm_id(crm_contact.get('id'))
                
                return {
                    "id": local_contact.id if local_contact else crm_contact.get('id'),
                    "name": crm_contact.get('name'),
                    "email": crm_contact.get('emails', [{}])[0].get('value') if crm_contact.get('emails') else None,
                    "phone": crm_contact.get('phones', [{}])[0].get('value') if crm_contact.get('phones') else None,
                    "crm_id": crm_contact.get('id'),
                    "source": "pipedrive"
                }
        except Exception as e:
            logger.warning(f"[{correlation_id}] Error buscando en Pipedrive: {e}")
        
        # FALLBACK: Buscar en BD local PostgreSQL
        logger.info(f"[{correlation_id}] Buscando en BD local...")
        
        # Buscar por email exacto
        contact = self.repository.get_by_email(query)
        
        # Si no se encuentra, buscar por nombre parcial
        if not contact:
            contact = self.repository.get_by_name(query)
        
        # Si no se encuentra, buscar por teléfono
        if not contact:
            contact = self.repository.get_by_phone(query)
        
        if not contact:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontró contacto con: {query}"
            )
        
        logger.info(f"[{correlation_id}] Contacto encontrado en BD local: {contact.id}")
        
        return {
            "id": contact.id,
            "name": contact.name,
            "email": contact.email,
            "phone": contact.phone,
            "crm_id": contact.crm_id,
            "source": "local"
        }
    
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
            # Obtener el contacto de BD local para conseguir el crm_id
            contact = self.repository.get_by_id(note.contact_id)
            if not contact:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No se encontró el contacto con ID {note.contact_id}"
                )
            
            # PRIMERO: Intentar agregar nota en Pipedrive usando crm_id
            logger.info(f"[{correlation_id}] Intentando agregar nota en Pipedrive...")
            crm_success = False
            note_id = None
            
            if contact.crm_id:
                try:
                    result = self.repository.add_note_to_crm(
                        contact_id=contact.crm_id,  # Usar crm_id en lugar de ID local
                        content=note.content
                    )
                    crm_success = True
                    note_id = result.get("id")
                    logger.info(f"[{correlation_id}] Nota agregada en Pipedrive: ID={note_id}")
                except Exception as crm_err:
                    logger.warning(f"[{correlation_id}] CRM falló: {crm_err}")
            else:
                logger.warning(f"[{correlation_id}] Contacto no tiene crm_id, solo se guarda localmente")
            
            logger.info(f"[{correlation_id}] Nota creada para contacto: {note.contact_id}")
            
            return ContactResponse(
                success=True,
                message=f"Nota agregada al contacto {contact.name}{' en Pipedrive' if crm_success else ' (solo localmente)'}",
                contact_id=note.contact_id,
                crm_id=contact.crm_id,
                url=f"https://app.pipedrive.com/person/{contact.crm_id}" if contact.crm_id else None,
                correlation_id=correlation_id
            )
        
        except HTTPException:
            raise
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
            # Obtener el contacto de BD local para conseguir el crm_id
            contact = self.repository.get_by_id(update.contact_id)
            if not contact:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No se encontró el contacto con ID {update.contact_id}"
                )
            
            # PRIMERO: Intentar actualizar en Pipedrive usando crm_id
            logger.info(f"[{correlation_id}] Intentando actualizar contacto en Pipedrive...")
            crm_success = False
            
            if contact.crm_id:
                try:
                    crm_result = self.repository.update_in_crm(
                        contact_id=contact.crm_id,  # Usar crm_id en lugar de ID local
                        fields=fields
                    )
                    crm_success = True
                    logger.info(f"[{correlation_id}] Contacto actualizado en Pipedrive")
                except Exception as crm_err:
                    logger.warning(f"[{correlation_id}] CRM falló: {crm_err}")
            else:
                logger.warning(f"[{correlation_id}] Contacto no tiene crm_id, solo se actualiza localmente")
            
            # SIEMPRE actualizar en PostgreSQL
            result = self.repository.update(
                contact_id=update.contact_id,
                **fields
            )
            
            logger.info(f"[{correlation_id}] Contacto actualizado: ID={update.contact_id}")
            
            return ContactResponse(
                success=True,
                message=f"Contacto {result.name} actualizado{' en Pipedrive' if crm_success else ' (solo localmente)'}",
                contact_id=update.contact_id,
                name=result.name,
                email=result.email,
                phone=result.phone,
                crm_id=result.crm_id,
                url=f"https://app.pipedrive.com/person/{result.crm_id}" if result.crm_id else None,
                correlation_id=correlation_id
            )
        
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"[{correlation_id}] Error actualizando contacto: {e}")
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Error al actualizar el contacto"
            )
