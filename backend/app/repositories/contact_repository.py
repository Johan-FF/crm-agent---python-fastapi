"""
Repository para contactos (Capa de acceso a datos)
"""
from typing import Optional, Dict, Any
import requests
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)


class ContactRepository:
    """
    Repositorio para operaciones CRUD de contactos en Pipedrive
    Abstrae la lógica de comunicación con la API de Pipedrive
    """
    
    def __init__(self):
        self.base_url = settings.PIPEDRIVE_BASE_URL
        self.api_key = settings.PIPEDRIVE_API_KEY
    
    def create(self, name: str, email: Optional[str] = None, phone: Optional[str] = None) -> Dict[str, Any]:
        """
        Crea un contacto en Pipedrive
        
        Args:
            name: Nombre del contacto
            email: Email (opcional)
            phone: Teléfono (opcional)
            
        Returns:
            Dict con datos del contacto creado
        """
        if not self.api_key:
            logger.warning("[MOCK] Creando contacto (sin credenciales)")
            return {
                "id": hash(name) % 100000,
                "name": name,
                "email": email,
                "phone": phone
            }
        
        try:
            url = f"{self.base_url}/persons"
            payload = {
                "name": name,
                "api_token": self.api_key
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
            
            return data["data"]
        
        except Exception as e:
            logger.error(f"Error creando contacto en repositorio: {e}")
            raise
    
    def get_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Busca un contacto por email
        
        Args:
            email: Email del contacto
            
        Returns:
            Dict con datos del contacto o None
        """
        if not self.api_key:
            logger.warning(f"[MOCK] Buscando contacto por email: {email}")
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
            logger.error(f"Error buscando contacto por email: {e}")
            return None
    
    def get_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Busca un contacto por nombre
        
        Args:
            name: Nombre del contacto
            
        Returns:
            Dict con datos del contacto o None
        """
        if not self.api_key:
            logger.warning(f"[MOCK] Buscando contacto por nombre: {name}")
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
            logger.error(f"Error buscando contacto por nombre: {e}")
            return None
    
    def add_note(self, contact_id: int, content: str) -> Dict[str, Any]:
        """
        Agrega una nota a un contacto
        
        Args:
            contact_id: ID del contacto
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
            url = f"{self.base_url}/notes"
            payload = {
                "content": content,
                "person_id": contact_id,
                "api_token": self.api_key
            }
            
            resp = requests.post(url, json=payload, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            
            if not data.get("success"):
                raise ValueError(f"Error en Pipedrive: {data.get('error')}")
            
            return data["data"]
        
        except Exception as e:
            logger.error(f"Error agregando nota en repositorio: {e}")
            raise
    
    def update(self, contact_id: int, fields: Dict[str, Any]) -> Dict[str, Any]:
        """
        Actualiza un contacto
        
        Args:
            contact_id: ID del contacto
            fields: Campos a actualizar
            
        Returns:
            Dict con datos del contacto actualizado
        """
        if not self.api_key:
            logger.warning(f"[MOCK] Actualizando contacto {contact_id}")
            return {"id": contact_id, **fields}
        
        try:
            url = f"{self.base_url}/persons/{contact_id}"
            payload = {
                "api_token": self.api_key,
                **fields
            }
            
            resp = requests.put(url, json=payload, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            
            if not data.get("success"):
                raise ValueError(f"Error en Pipedrive: {data.get('error')}")
            
            return data["data"]
        
        except Exception as e:
            logger.error(f"Error actualizando contacto en repositorio: {e}")
            raise
