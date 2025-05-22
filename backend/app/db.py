# backend/app/db.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# по-умолчанию sqlite, но можно переопределить через env переменную
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./dev.db")

# для sqlite нужен этот параметр
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """
    Зависимость FastAPI — отдаёт сессию и закрывает её по завершении.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
