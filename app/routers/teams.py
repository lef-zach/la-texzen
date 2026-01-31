from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.models import User, Team, TeamMember
from app.schemas import TeamCreate
from app.dependencies import get_current_user

router = APIRouter()

@router.post("/teams")
async def create_team(team: TeamCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_team = Team(
        name=team.name,
        description=team.description,
        created_by=current_user.id,
        created_at=datetime.utcnow()
    )
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    
    db_team_member = TeamMember(
        team_id=db_team.id,
        user_id=current_user.id,
        role="owner",
        joined_at=datetime.utcnow()
    )
    db.add(db_team_member)
    db.commit()
    
    return {
        "id": db_team.id,
        "name": db_team.name,
        "description": db_team.description,
        "created_by": db_team.created_by,
        "created_at": db_team.created_at
    }

@router.get("/teams")
async def get_teams(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    team_members = db.query(TeamMember).filter(TeamMember.user_id == current_user.id).all()
    teams = []
    
    for member in team_members:
        team = db.query(Team).filter(Team.id == member.team_id).first()
        if team:
            teams.append({
                "id": team.id,
                "name": team.name,
                "description": team.description,
                "role": member.role,
                "joined_at": member.joined_at
            })
    
    return teams

@router.get("/teams/{team_id}")
async def get_team(team_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    team_member = db.query(TeamMember).filter(
        TeamMember.team_id == team_id,
        TeamMember.user_id == current_user.id
    ).first()
    
    if not team_member:
        raise HTTPException(status_code=403, detail="Not authorized to access this team")
    
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    return {
        "id": team.id,
        "name": team.name,
        "description": team.description,
        "created_by": team.created_by,
        "created_at": team.created_at
    }

@router.post("/teams/{team_id}/join")
async def join_team(team_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    existing_member = db.query(TeamMember).filter(
        TeamMember.team_id == team_id,
        TeamMember.user_id == current_user.id
    ).first()
    
    if existing_member:
        raise HTTPException(status_code=400, detail="Already a member of this team")
    
    db_team_member = TeamMember(
        team_id=team_id,
        user_id=current_user.id,
        role="member",
        joined_at=datetime.utcnow()
    )
    db.add(db_team_member)
    db.commit()
    
    return {"message": "Successfully joined the team"}

@router.post("/teams/{team_id}/leave")
async def leave_team(team_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    team_member = db.query(TeamMember).filter(
        TeamMember.team_id == team_id,
        TeamMember.user_id == current_user.id
    ).first()
    
    if not team_member:
        raise HTTPException(status_code=400, detail="Not a member of this team")
    
    if team_member.role == "owner":
        raise HTTPException(status_code=400, detail="Owner cannot leave the team. Transfer ownership first.")
    
    db.delete(team_member)
    db.commit()
    
    return {"message": "Successfully left the team"}

@router.get("/teams/{team_id}/members")
async def get_team_members(team_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    team_member = db.query(TeamMember).filter(
        TeamMember.team_id == team_id,
        TeamMember.user_id == current_user.id
    ).first()
    
    if not team_member:
        raise HTTPException(status_code=403, detail="Not authorized to access this team")
    
    members = db.query(TeamMember).filter(TeamMember.team_id == team_id).all()
    
    result = []
    for member in members:
        user = db.query(User).filter(User.id == member.user_id).first()
        if user:
            result.append({
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "role": member.role,
                "joined_at": member.joined_at
            })
    
    return result

@router.delete("/teams/{team_id}/members/{user_id}")
async def remove_team_member(team_id: int, user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    current_member = db.query(TeamMember).filter(
        TeamMember.team_id == team_id,
        TeamMember.user_id == current_user.id
    ).first()
    
    if not current_member or current_member.role not in ["owner", "admin"]:
        raise HTTPException(status_code=403, detail="Not authorized to remove members")
    
    target_member = db.query(TeamMember).filter(
        TeamMember.team_id == team_id,
        TeamMember.user_id == user_id
    ).first()
    
    if not target_member:
        raise HTTPException(status_code=404, detail="User is not a member of this team")
    
    if target_member.role == "owner":
        raise HTTPException(status_code=400, detail="Cannot remove team owner")
    
    db.delete(target_member)
    db.commit()
    
    return {"message": "Successfully removed member from team"}