"""
Gestión de sesiones de base de datos con SQLAlchemy
"""
from typing import AsyncGenerator, Generator
from sqlalchemy.orm import Session
from app.db.base import SessionLocal, init_db, close_db


def get_db() -> Generator[Session, None, None]:
    """
    Dependencia para inyectar la sesión de base de datos en endpoints
    Uso: db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
