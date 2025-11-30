"""
FastAPI Backend para Verticcal CRM Agent

NOTA: Este archivo ahora importa la aplicación del módulo refactorizado.
La arquitectura ha sido refactorizada en una estructura modular bajo app/
manteniendo backward compatibility con los endpoints originales.
"""

# Importar la aplicación FastAPI del módulo refactorizado
from app.main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)
