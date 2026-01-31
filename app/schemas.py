from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class TeamBase(BaseModel):
    name: str
    description: Optional[str] = None

class TeamCreate(TeamBase):
    pass

class Team(TeamBase):
    id: int
    created_by: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class TemplateBase(BaseModel):
    name: str
    content: str
    visibility: str  # public, private, team

class TemplateCreate(TemplateBase):
    pass

class Template(TemplateBase):
    id: int
    type: str  # global, user, team
    owner_id: Optional[int] = None
    team_id: Optional[int] = None
    category_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class DocumentBase(BaseModel):
    title: str
    content: str
    template_id: Optional[int] = None
    visibility: str  # personal, team, public

class DocumentCreate(DocumentBase):
    pass

class Document(DocumentBase):
    id: int
    owner_id: int
    team_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class CitationBase(BaseModel):
    citation_key: str
    citation_data: str

class CitationCreate(CitationBase):
    pass

class Citation(CitationBase):
    id: int
    document_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class DocumentVersionBase(BaseModel):
    content: str
    version_number: int

class DocumentVersionCreate(DocumentVersionBase):
    pass

class DocumentVersion(DocumentVersionBase):
    id: int
    document_id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class DocumentCommentBase(BaseModel):
    content: str
    parent_id: Optional[int] = None

class DocumentCommentCreate(DocumentCommentBase):
    pass

class DocumentComment(DocumentCommentBase):
    id: int
    document_id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class TemplateCategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class TemplateCategoryCreate(TemplateCategoryBase):
    pass

class TemplateCategory(TemplateCategoryBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class FileUpload(BaseModel):
    file: str
    filename: str
    format: str

class ProcessingResult(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None

class ErrorResponse(BaseModel):
    detail: str

class SuccessResponse(BaseModel):
    message: str
    data: Optional[dict] = None
