from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# SQLite database file path
DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "edupulse.db")
DATABASE_URL = f"sqlite:///{DB_FILE}"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create a scoped session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()

def init_db():
    """
    Initialize the database by creating all tables defined in models.
    """
    import models  # Import models here to ensure they are registered with Base
    Base.metadata.create_all(bind=engine)
    
    # Pre-create default teacher credentials
    db = SessionLocal()
    import auth
    if not auth.get_user(db, "teacher@edupulse.com"):
        auth.create_user(db, "Admin Teacher", "teacher@edupulse.com", "teacher123", "teacher")
        
    # Pre-create 10 sample student accounts
    for i in range(1, 11):
        email = f"student{i}@edupulse.com"
        if not auth.get_user(db, email):
            auth.create_user(db, f"Student {i}", email, f"student{i}", "student")
            
    db.close()

def get_db_session():
    """
    Get a new database session.
    """
    db = SessionLocal()
    try:
        return db
    finally:
        # Note: We rely on the caller to close the session or use it in a context manager
        pass
