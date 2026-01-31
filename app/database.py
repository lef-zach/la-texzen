from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# Create engine
engine = create_engine(DATABASE_URL)

# Create session local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base model
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create database tables
def create_tables():
    from app.models import User, Team, Template, Document, TemplateCategory, TeamMember, Citation, DocumentVersion, DocumentComment
    
    User.metadata.create_all(bind=engine)
    Team.metadata.create_all(bind=engine)
    Template.metadata.create_all(bind=engine)
    Document.metadata.create_all(bind=engine)
    TemplateCategory.metadata.create_all(bind=engine)
    TeamMember.metadata.create_all(bind=engine)
    Citation.metadata.create_all(bind=engine)
    DocumentVersion.metadata.create_all(bind=engine)
    DocumentComment.metadata.create_all(bind=engine)

# Initialize database
if __name__ == "__main__":
    create_tables()
