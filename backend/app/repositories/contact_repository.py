"""
Repository para contactos - Capa de acceso a datos
Maneja tanto la base de datos local (PostgreSQL) como la API de Pipedrive
"""
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import requests
import logging

from app.core.config import settings
from app.models.contact import Contact

logger = logging.getLogger(__name__)


class ContactRepository:
    """
    Repositorio para operaciones CRUD de contactos
    - Guarda en base de datos PostgreSQL
    - Sincroniza con Pipedrive API cuando está disponible
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.base_url = settings.PIPEDRIVE_BASE_URL
        self.api_key = settings.PIPEDRIVE_API_KEY
    
    # ================== OPERACIONES CON BD LOCAL ==================
    
    def create_local(self, name: str, email: Optional[str] = None, 
                    phone: Optional[str] = None, crm_id: Optional[int] = None) -> Contact:
        """
        Crea un contacto en la base de datos local PostgreSQL
        
        Args:
            name: Nombre del contacto
            email: Email (opcional)
            phone: Teléfono (opcional)
            crm_id: ID en Pipedrive (opcional)
            
        Returns:
            Contact: Objeto Contact creado
        """
        try:
            contact = Contact(
                name=name,
                email=email,
                phone=phone,
                crm_id=crm_id
            )
            self.db.add(contact)
            self.db.commit()
            self.db.refresh(contact)
            logger.info(f"Contacto creado en BD: {contact.id} - {name}")
            return contact
        except IntegrityError as e:
            self.db.rollback()
            logger.error(f"Error de integridad al crear contacto: {e}")
            raise
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creando contacto en BD: {e}")
            raise
    
    def get_by_id(self, contact_id: int) -> Optional[Contact]:
        """
        Obtiene un contacto por su ID en BD
        """
        return self.db.query(Contact).filter(Contact.id == contact_id).first()
    
    def get_by_email(self, email: str) -> Optional[Contact]:
        """
        Obtiene un contacto por email en BD
        """
        return self.db.query(Contact).filter(Contact.email == email).first()
    
    def get_by_crm_id(self, crm_id: int) -> Optional[Contact]:
        """
        Obtiene un contacto por su ID en Pipedrive
        """
        return self.db.query(Contact).filter(Contact.crm_id == crm_id).first()
    
    def get_by_name(self, name: str) -> Optional[Contact]:
        """
        Busca contactos por nombre (contiene)
        """
        return self.db.query(Contact).filter(
            Contact.name.ilike(f"%{name}%")
        ).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Contact]:
        """
        Obtiene todos los contactos con paginación
        """
        return self.db.query(Contact).offset(skip).limit(limit).all()
    
    def update(self, contact_id: int, **fields) -> Optional[Contact]:
        """
        Actualiza un contacto en BD
        
        Args:
            contact_id: ID del contacto
            **fields: Campos a actualizar (name, email, phone, crm_id)
            
        Returns:
            Contact actualizado o None
        """
        try:
            contact = self.get_by_id(contact_id)
            if not contact:
                return None
            
            for key, value in fields.items():
                if hasattr(contact, key) and key not in ['id', 'created_at']:
                    setattr(contact, key, value)
            
            self.db.commit()
            self.db.refresh(contact)
            logger.info(f"Contacto actualizado: {contact_id}")
            return contact
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error actualizando contacto: {e}")
            raise
    
    def delete(self, contact_id: int) -> bool:
        """
        Elimina un contacto de BD
        """
        try:
            contact = self.get_by_id(contact_id)
            if contact:
                self.db.delete(contact)
                self.db.commit()
                logger.info(f"Contacto eliminado: {contact_id}")
                return True
            return False
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error eliminando contacto: {e}")
            raise
    
    def add_note(self, contact_id: int, content: str) -> Dict[str, Any]:
        """
        Agrega una nota a un contacto (intenta en Pipedrive si está disponible)
        """
        try:
            # Intentar agregar nota en Pipedrive si hay API key
            return self.add_note_to_crm(contact_id, content)
        except Exception as e:
            logger.warning(f"No se pudo agregar nota en Pipedrive: {e}")
            # Retornar respuesta mock si falla
            return {
                "id": contact_id,
                "content": content
            }
    
    # ================== OPERACIONES CON PIPEDRIVE CRM ==================
    
    def create_in_crm(self, name: str, email: Optional[str] = None, 
                     phone: Optional[str] = None) -> Dict[str, Any]:
        """
        Crea un contacto en Pipedrive
        
        Args:
            name: Nombre del contacto
            email: Email (opcional)
            phone: Teléfono (opcional)
            
        Returns:
            Dict con datos del contacto creado en Pipedrive
        """
        if not self.api_key:
            logger.warning("[MOCK] Creando contacto en Pipedrive (sin credenciales)")
            return {
                "id": hash(name) % 100000,
                "name": name,
                "email": email,
                "phone": phone
            }
        
        try:
            url = f"{self.base_url}/persons?api_token={self.api_key}"
            payload = {
                "name": name
            }
            
            if email:
                payload["email"] = email
            if phone:
                payload["phone"] = phone
            
            resp = requests.post(url, json=payload, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            
            if not data.get("success"):
                raise ValueError(f"Error en Pipedrive: {data.get('error')}")
            
            logger.info(f"Contacto creado en Pipedrive: {data['data']['id']}")
            return data["data"]
        
        except Exception as e:
            logger.error(f"Error creando contacto en Pipedrive: {e}")
            raise
    
    def get_by_email_from_crm(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Busca un contacto por email en Pipedrive
        """
        if not self.api_key:
            logger.info(f"[MOCK] Buscando contacto en Pipedrive por email: {email}")
            return None
        
        try:
            url = f"{self.base_url}/persons/search"
            params = {
                "term": email,
                "api_token": self.api_key
            }
            
            resp = requests.get(url, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            
            if data.get("success") and data.get("data", {}).get("items"):
                for item in data["data"]["items"]:
                    contact = item.get("item", {})
                    if contact.get("email"):
                        for email_info in contact["email"]:
                            if email_info.get("value") == email:
                                return contact
            
            return None
        
        except Exception as e:
            logger.error(f"Error buscando contacto en Pipedrive por email: {e}")
            return None
    
    def get_by_name_from_crm(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Busca un contacto por nombre en Pipedrive
        """
        if not self.api_key:
            logger.info(f"[MOCK] Buscando contacto en Pipedrive por nombre: {name}")
            return None
        
        try:
            url = f"{self.base_url}/persons/search"
            params = {
                "term": name,
                "api_token": self.api_key
            }
            
            resp = requests.get(url, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            
            if data.get("success") and data.get("data", {}).get("items"):
                return data["data"]["items"][0]["item"]
            
            return None
        
        except Exception as e:
            logger.error(f"Error buscando contacto en Pipedrive por nombre: {e}")
            return None
    
    def add_note_to_crm(self, contact_id: int, content: str) -> Dict[str, Any]:
        """
        Agrega una nota a un contacto en Pipedrive
        
        Args:
            contact_id: ID del contacto en Pipedrive
            content: Contenido de la nota
            
        Returns:
            Dict con datos de la nota creada
        """
        if not self.api_key:
            logger.warning(f"[MOCK] Agregando nota a contacto {contact_id}")
            return {
                "id": hash(content) % 100000,
                "person_id": contact_id,
                "content": content
            }
        
        try:
            url = f"{self.base_url}/notes?api_token={self.api_key}"
            payload = {
                "content": content,
                "person_id": contact_id
            }
            
            resp = requests.post(url, json=payload, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            
            if not data.get("success"):
                raise ValueError(f"Error en Pipedrive: {data.get('error')}")
            
            logger.info(f"Nota agregada a contacto {contact_id}")
            return data["data"]
        
        except Exception as e:
            logger.error(f"Error agregando nota en Pipedrive: {e}")
            raise
    
    def update_in_crm(self, contact_id: int, fields: Dict[str, Any]) -> Dict[str, Any]:
        """
        Actualiza un contacto en Pipedrive
        
        Args:
            contact_id: ID del contacto en Pipedrive
            fields: Campos a actualizar
            
        Returns:
            Dict con datos del contacto actualizado
        """
        if not self.api_key:
            logger.warning(f"[MOCK] Actualizando contacto {contact_id}")
            return {"id": contact_id, **fields}
        
        try:
            url = f"{self.base_url}/persons/{contact_id}?api_token={self.api_key}"
            payload = {
                **fields
            }
            
            resp = requests.put(url, json=payload, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            
            if not data.get("success"):
                raise ValueError(f"Error en Pipedrive: {data.get('error')}")
            
            logger.info(f"Contacto actualizado en Pipedrive: {contact_id}")
            return data["data"]
        
        except Exception as e:
            logger.error(f"Error actualizando contacto en Pipedrive: {e}")
            raise
