"""
Schemas Pydantic para validación de requests/responses
"""
from typing import Optional, Dict, Any
from pydantic import BaseModel, EmailStr, Field


class ContactCreate(BaseModel):
    """Schema para crear un contacto"""
    name: str = Field(..., min_length=1, description="Nombre del contacto")
    email: Optional[EmailStr] = Field(None, description="Email del contacto")
    phone: Optional[str] = Field(None, description="Teléfono del contacto")
    
    class Config:
        examples = [
            {
                "name": "Falcao García",
                "email": "falcao@ .com",
                "phone": "+57 300 123 4567"
            }
        ]


class ContactUpdate(BaseModel):
    """Schema para actualizar un contacto"""
    contact_id: int = Field(..., description="ID del contacto")
    fields: Dict[str, Any] = Field(..., description="Campos a actualizar")
    
    class Config:
        examples = [
            {
                "contact_id": 123,
                "fields": {"phone": "+57 311 999 0000", "status": "Qualified"}
            }
        ]


class ContactResponse(BaseModel):
    """Schema de respuesta para operaciones con contactos"""
    success: bool = Field(..., description="Indica si la operación fue exitosa")
    message: str = Field(..., description="Mensaje de respuesta")
    contact_id: Optional[int] = Field(None, description="ID del contacto")
    crm_id: Optional[int] = Field(None, description="ID en el CRM")
    url: Optional[str] = Field(None, description="URL del contacto en el CRM")
    correlation_id: str = Field(..., description="ID para rastrear la operación")


class NoteCreate(BaseModel):
    """Schema para crear una nota"""
    contact_id: int = Field(..., description="ID del contacto")
    content: str = Field(..., min_length=1, description="Contenido de la nota")
    
    class Config:
        examples = [
            {
                "contact_id": 123,
                "content": "Cliente interesado en plan Premium"
            }
        ]


class HealthResponse(BaseModel):
    """Schema de respuesta del health check"""
    status: str = Field(..., description="Estado del servicio")
    timestamp: str = Field(..., description="Timestamp ISO")
    crm_configured: bool = Field(..., description="¿CRM está configurado?")
