from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
import os
import shutil
from datetime import datetime
import uuid

from app.database import get_db
from app.models import User
from app.dependencies import get_current_user

router = APIRouter()

# File upload directory
UPLOAD_DIR = "documents/uploads"
TEMP_DIR = "tmp"

# Ensure directories exist
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

# Supported file formats
SUPPORTED_FORMATS = {
    '.pdf': 'PDF',
    '.docx': 'DOCX',
    '.doc': 'DOC',
    '.txt': 'TXT',
    '.tex': 'LATEX',
    '.jpg': 'IMAGE',
    '.jpeg': 'IMAGE',
    '.png': 'IMAGE',
    '.tiff': 'IMAGE',
    '.tif': 'IMAGE'
}

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Validate file format
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in SUPPORTED_FORMATS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file format: {file_ext}. Supported formats: {', '.join(SUPPORTED_FORMATS.keys())}"
        )
    
    # Generate unique filename
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    # Save file
    try:
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error saving file: {str(e)}"
        )
    
    # Get file size
    file_size = os.path.getsize(file_path)
    
    return {
        "message": "File uploaded successfully",
        "filename": unique_filename,
        "original_filename": file.filename,
        "file_format": SUPPORTED_FORMATS[file_ext],
        "file_size": file_size,
        "file_path": file_path,
        "uploaded_at": datetime.utcnow()
    }

@router.get("/upload/{filename}")
async def get_uploaded_file(
    filename: str,
    current_user: User = Depends(get_current_user)
):
    # Validate filename
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    # Return file info
    file_size = os.path.getsize(file_path)
    file_ext = os.path.splitext(filename)[1].lower()
    
    return {
        "filename": filename,
        "file_format": SUPPORTED_FORMATS.get(file_ext, "UNKNOWN"),
        "file_size": file_size,
        "file_path": file_path
    }

@router.delete("/upload/{filename}")
async def delete_uploaded_file(
    filename: str,
    current_user: User = Depends(get_current_user)
):
    # Validate filename
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    # Delete file
    try:
        os.remove(file_path)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting file: {str(e)}"
        )
    
    return {"message": "File deleted successfully"}

@router.post("/upload/temp")
async def upload_temp_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    # Generate unique filename
    file_ext = os.path.splitext(file.filename)[1].lower()
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(TEMP_DIR, unique_filename)
    
    # Save file temporarily
    try:
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error saving temporary file: {str(e)}"
        )
    
    return {
        "message": "Temporary file uploaded successfully",
        "filename": unique_filename,
        "file_path": file_path
    }

@router.delete("/temp/{filename}")
async def delete_temp_file(
    filename: str,
    current_user: User = Depends(get_current_user)
):
    # Validate filename
    file_path = os.path.join(TEMP_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Temporary file not found"
        )
    
    # Delete file
    try:
        os.remove(file_path)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting temporary file: {str(e)}"
        )
    
    return {"message": "Temporary file deleted successfully"}