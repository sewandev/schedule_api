from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import create_engine, MetaData
from app.core.config import settings

# Global metadata configuration
metadata = MetaData()

# Declarative Base
class Base(DeclarativeBase):
    metadata = metadata

# Database engine
engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Test database connection
def test_connection():
    try:
        with engine.connect() as connection:
            print("Database connection successful!")
    except Exception as e:
        print(f"Database connection failed: {e}")
