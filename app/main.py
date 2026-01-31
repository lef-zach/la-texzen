from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import jwt
import os

from .database import get_db, SessionLocal, engine, Base
from .models import User, Team, Template, Document, TeamMember, TemplateCategory, Citation, DocumentVersion, DocumentComment
from .schemas import UserCreate, UserLogin, Token, TemplateCreate, DocumentCreate
from .hashing import Hash
from .dependencies import get_current_user

# Create database tables
User.metadata.create_all(bind=engine)
Team.metadata.create_all(bind=engine)
Template.metadata.create_all(bind=engine)
Document.metadata.create_all(bind=engine)
TemplateCategory.metadata.create_all(bind=engine)
TeamMember.metadata.create_all(bind=engine)
Citation.metadata.create_all(bind=engine)
DocumentVersion.metadata.create_all(bind=engine)
DocumentComment.metadata.create_all(bind=engine)

app = FastAPI(
    title="Scientific Paper Converter",
    description="Web application for converting documents to scientific paper formats",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# JWT configuration
SECRET_KEY = "your-secret-key-here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Authentication functions
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = verify_token(token)
    if payload is None:
        raise credentials_exception
    
    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise credentials_exception
    
    return db_user

# Routes
@app.get("/")
async def root():
    return {"message": "Scientific Paper Converter API"}

@app.post("/register", response_model=Token)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = Hash().hash(user.password)
    db_user = User(
        email=user.email,
        password=hashed_password,
        name=user.name,
        created_at=datetime.utcnow()
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    access_token = create_access_token(data={"sub": str(db_user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == form_data.username).first()
    if db_user is None:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    user = User(**db_user.__dict__)
    if not Hash().verify(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=dict)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.name,
        "created_at": current_user.created_at
    }

@app.post("/teams")
async def create_team(team: dict, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_team = Team(
        name=team["name"],
        description=team.get("description", ""),
        created_by=current_user.id,
        created_at=datetime.utcnow()
    )
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    
    # Add user as team member
    db_team_member = TeamMember(
        team_id=db_team.id,
        user_id=current_user.id,
        role="owner",
        joined_at=datetime.utcnow()
    )
    db.add(db_team_member)
    db.commit()
    
    return db_team

@app.post("/templates")
async def create_template(template: TemplateCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_template = Template(
        name=template.name,
        type="user",
        content=template.content,
        visibility="private",
        owner_id=current_user.id,
        created_at=datetime.utcnow()
    )
    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    
    return db_template

@app.post("/documents")
async def create_document(document: DocumentCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_document = Document(
        title=document.title,
        content=document.content,
        template_id=document.template_id,
        owner_id=current_user.id,
        visibility="personal",
        created_at=datetime.utcnow()
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    
    return db_document

@app.get("/templates")
async def get_templates(db: Session = Depends(get_db)):
    # Get global templates
    global_templates = db.query(Template).filter(Template.type == "global").all()
    
    templates = []
    for template in global_templates:
        templates.append({
            "id": template.id,
            "name": template.name,
            "type": template.type,
            "visibility": template.visibility,
            "owner_id": template.owner_id,
            "created_at": template.created_at
        })
    
    return templates

@app.get("/template-categories")
async def get_template_categories(db: Session = Depends(get_db)):
    categories = db.query(TemplateCategory).all()
    return categories

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)