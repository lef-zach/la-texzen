from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
import os

from app.database import get_db
from app.models import User, Document, Template
from app.schemas import DocumentCreate
from app.dependencies import get_current_user
from app.services.document_processing import document_processor
from app.services.template_manager import template_manager

router = APIRouter()

@router.post("/documents")
async def create_document(document: DocumentCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_document = Document(
        title=document.title,
        content=document.content,
        template_id=document.template_id,
        owner_id=current_user.id,
        visibility=document.visibility,
        created_at=datetime.utcnow()
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    
    return {
        "id": db_document.id,
        "title": db_document.title,
        "content": db_document.content,
        "template_id": db_document.template_id,
        "owner_id": db_document.owner_id,
        "visibility": db_document.visibility,
        "created_at": db_document.created_at
    }

@router.get("/documents")
async def get_documents(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Get user's documents
    documents = db.query(Document).filter(Document.owner_id == current_user.id).all()
    
    result = []
    for doc in documents:
        template = None
        if doc.template_id:
            template = db.query(Template).filter(Template.id == doc.template_id).first()
        
        result.append({
            "id": doc.id,
            "title": doc.title,
            "template_id": doc.template_id,
            "template_name": template.name if template else None,
            "visibility": doc.visibility,
            "created_at": doc.created_at,
            "updated_at": doc.updated_at
        })
    
    return result

@router.get("/documents/{document_id}")
async def get_document(document_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Check access
    if document.owner_id != current_user.id and document.visibility not in ["public"]:
        raise HTTPException(status_code=403, detail="Not authorized to access this document")
    
    template = None
    if document.template_id:
        template = db.query(Template).filter(Template.id == document.template_id).first()
    
    return {
        "id": document.id,
        "title": document.title,
        "content": document.content,
        "template_id": document.template_id,
        "template_name": template.name if template else None,
        "visibility": document.visibility,
        "created_at": document.created_at,
        "updated_at": document.updated_at
    }

@router.patch("/documents/{document_id}")
async def update_document(document_id: int, document_data: dict, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Check ownership
    if document.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this document")
    
    # Update fields
    if 'title' in document_data:
        document.title = document_data['title']
    if 'content' in document_data:
        document.content = document_data['content']
    if 'visibility' in document_data:
        document.visibility = document_data['visibility']
    
    document.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(document)
    
    return {
        "id": document.id,
        "title": document.title,
        "content": document.content,
        "visibility": document.visibility,
        "updated_at": document.updated_at
    }

@router.delete("/documents/{document_id}")
async def delete_document(document_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Check ownership
    if document.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this document")
    
    db.delete(document)
    db.commit()
    
    return {"message": "Document deleted successfully"}

@router.post("/documents/{document_id}/convert")
async def convert_document(document_id: int, target_format: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Check access
    if document.owner_id != current_user.id and document.visibility not in ["public"]:
        raise HTTPException(status_code=403, detail="Not authorized to convert this document")
    
    # Get template if available
    template = None
    if document.template_id:
        template = template_manager.get_template(document.template_id, db)
    
    # Apply template if available
    content = document.content
    if template:
        metadata = {
            'title': document.title,
            'author': current_user.name
        }
        content = template_manager.apply_template(document.template_id, content, metadata, db)
    
    # Create temporary file
    temp_file = f"temp_{document_id}.tex"
    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    try:
        # Process document
        result = document_processor.process_document(temp_file, target_format)
        
        if result['success']:
            return {
                "success": True,
                "message": f"Document converted to {target_format} successfully",
                "data": {
                    "content": result['data']['content'] if result['data'] else None,
                    "format": target_format,
                    "metadata": result['data']['metadata'] if result['data'] else None
                }
            }
        else:
            raise HTTPException(status_code=500, detail=result['message'])
    
    finally:
        # Cleanup temporary file
        if os.path.exists(temp_file):
            os.remove(temp_file)

@router.get("/documents/{document_id}/export")
async def export_document(document_id: int, format: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Check access
    if document.owner_id != current_user.id and document.visibility not in ["public"]:
        raise HTTPException(status_code=403, detail="Not authorized to export this document")
    
    # Process document based on format
    if format == 'tex':
        return {
            "success": True,
            "content": document.content,
            "format": "tex"
        }
    elif format == 'pdf':
        # Use document processing service to compile to PDF
        temp_file = f"temp_{document_id}.tex"
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(document.content)
        
        try:
            result = document_processor.process_document(temp_file, 'pdf')
            if result['success']:
                return {
                    "success": True,
                    "content": result['data']['content'],
                    "format": "pdf"
                }
            else:
                raise HTTPException(status_code=500, detail=result['message'])
        finally:
            # Cleanup temporary file
            if os.path.exists(temp_file):
                os.remove(temp_file)
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported export format: {format}")