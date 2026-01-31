from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.models import User, Team, TeamMember, Template, TemplateCategory
from app.schemas import TemplateCreate, TemplateCategoryCreate

router = APIRouter()

@router.post("/templates")
async def create_template(template: TemplateCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_template = Template(
        name=template.name,
        type="user",
        content=template.content,
        visibility=template.visibility,
        owner_id=current_user.id,
        created_at=datetime.utcnow()
    )
    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    
    return {
        "id": db_template.id,
        "name": db_template.name,
        "type": db_template.type,
        "visibility": db_template.visibility,
        "owner_id": db_template.owner_id,
        "created_at": db_template.created_at
    }

@router.get("/templates")
async def get_templates(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Get global templates
    global_templates = db.query(Template).filter(Template.type == "global").all()
    
    # Get user's private templates
    user_templates = db.query(Template).filter(
        Template.type == "user",
        Template.owner_id == current_user.id,
        Template.visibility == "private"
    ).all()
    
    # Get user's team templates
    team_ids = db.query(TeamMember.team_id).filter(TeamMember.user_id == current_user.id).all()
    team_templates = []
    if team_ids:
        team_ids = [t[0] for t in team_ids]
        team_templates = db.query(Template).filter(
            Template.type == "team",
            Template.team_id.in_(team_ids)
        ).all()
    
    # Get user's public templates
    public_templates = db.query(Template).filter(
        Template.type == "user",
        Template.owner_id == current_user.id,
        Template.visibility == "public"
    ).all()
    
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
    
    for template in user_templates:
        templates.append({
            "id": template.id,
            "name": template.name,
            "type": template.type,
            "visibility": template.visibility,
            "owner_id": template.owner_id,
            "created_at": template.created_at
        })
    
    for template in team_templates:
        templates.append({
            "id": template.id,
            "name": template.name,
            "type": template.type,
            "visibility": template.visibility,
            "owner_id": template.owner_id,
            "team_id": template.team_id,
            "created_at": template.created_at
        })
    
    for template in public_templates:
        templates.append({
            "id": template.id,
            "name": template.name,
            "type": template.type,
            "visibility": template.visibility,
            "owner_id": template.owner_id,
            "created_at": template.created_at
        })
    
    return templates

@router.get("/templates/{template_id}")
async def get_template(template_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    template = db.query(Template).filter(Template.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    # Check access
    if template.type == "global":
        pass  # Public access
    elif template.type == "user":
        if template.owner_id != current_user.id and template.visibility != "public":
            raise HTTPException(status_code=403, detail="Not authorized to access this template")
    elif template.type == "team":
        team_member = db.query(TeamMember).filter(
            TeamMember.team_id == template.team_id,
            TeamMember.user_id == current_user.id
        ).first()
        if not team_member:
            raise HTTPException(status_code=403, detail="Not authorized to access this template")
    
    return {
        "id": template.id,
        "name": template.name,
        "type": template.type,
        "content": template.content,
        "visibility": template.visibility,
        "owner_id": template.owner_id,
        "team_id": template.team_id,
        "created_at": template.created_at,
        "updated_at": template.updated_at
    }

@router.patch("/templates/{template_id}/visibility")
async def update_template_visibility(template_id: int, visibility: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    template = db.query(Template).filter(Template.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    # Check ownership
    if template.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this template")
    
    # Validate visibility
    if visibility not in ["public", "private", "team"]:
        raise HTTPException(status_code=400, detail="Invalid visibility. Must be 'public', 'private', or 'team'")
    
    template.visibility = visibility
    db.commit()
    
    return {
        "id": template.id,
        "name": template.name,
        "visibility": template.visibility
    }

@router.delete("/templates/{template_id}")
async def delete_template(template_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    template = db.query(Template).filter(Template.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    # Check ownership
    if template.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this template")
    
    db.delete(template)
    db.commit()
    
    return {"message": "Template deleted successfully"}

# Template categories
@router.post("/template-categories")
async def create_template_category(category: TemplateCategoryCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_category = TemplateCategory(
        name=category.name,
        description=category.description,
        created_at=datetime.utcnow()
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    
    return {
        "id": db_category.id,
        "name": db_category.name,
        "description": db_category.description,
        "created_at": db_category.created_at
    }

@router.get("/template-categories")
async def get_template_categories(db: Session = Depends(get_db)):
    categories = db.query(TemplateCategory).all()
    return categories