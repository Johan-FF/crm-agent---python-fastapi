"""
Modelos de datos para contactos (ORM)
"""
from typing import Optional
from datetime import datetime


class Contact:
    """
    Modelo de Contacto para la base de datos
    (Placeholder para ORM - SQLAlchemy, Tortoise, etc.)
    """
    
    def __init__(
        self,
        id: int,
        name: str,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        created_at: datetime = None,
        updated_at: datetime = None,
    ):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def __repr__(self):
        return f"<Contact(id={self.id}, name='{self.name}', email='{self.email}')>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
