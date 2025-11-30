"""
Configuración global de la aplicación
"""
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()


class Settings:
    """Configuración de la aplicación"""
    
    # API
    API_TITLE: str = "Verticcal CRM Agent API"
    API_DESCRIPTION: str = "Backend para orquestar n8n Chat Agent con CRM"
    API_VERSION: str = "2.0.0"
    
    # Pipedrive
    PIPEDRIVE_API_KEY: str = os.getenv("PIPEDRIVE_API_KEY", "")
    PIPEDRIVE_BASE_URL: str = os.getenv(
        "PIPEDRIVE_BASE_URL",
        "https://api.pipedrive.com/v1"
    )
    
    # Open Router (alternativa a OpenAI)
    OPEN_ROUTER_API_KEY: str = os.getenv("OPEN_ROUTER_API_KEY", "")
    OPEN_ROUTER_MODEL: str = os.getenv("OPEN_ROUTER_MODEL", "openai/gpt-3.5-turbo")
    
    # Database (para expansión futura)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # CORS
    CORS_ORIGINS: list = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list = ["*"]
    CORS_ALLOW_HEADERS: list = ["*"]
    
    @property
    def crm_configured(self) -> bool:
        """Verifica si el CRM está configurado"""
        return bool(self.PIPEDRIVE_API_KEY)
    
    @property
    def is_mock_mode(self) -> bool:
        """Retorna True si no hay credenciales de CRM configuradas"""
        return not self.crm_configured


# Instancia global de configuración
settings = Settings()
