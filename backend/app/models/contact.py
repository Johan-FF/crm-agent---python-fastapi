"""
Modelos ORM para contactos usando SQLAlchemy
"""
from sqlalchemy import Column, Integer, String, DateTime, func
from datetime import datetime
from app.db.base import Base


class Contact(Base):
    """
    Modelo de Contacto para PostgreSQL
    Tabla: contacts
    """
    __tablename__ = "contacts"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    email = Column(String(255), unique=True, index=True, nullable=True)
    phone = Column(String(20), nullable=True)
    crm_id = Column(Integer, unique=True, nullable=True, index=True)  # ID en Pipedrive
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<Contact(id={self.id}, name='{self.name}', email='{self.email}', crm_id={self.crm_id})>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "crm_id": self.crm_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
