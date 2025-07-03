# app/routes/ops.py

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from app import models, auth
from app.database import get_db
import os
import shutil

router = APIRouter()

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {".docx", ".pptx", ".xlsx"}

def allowed_file(filename: str):
    return any(filename.endswith(ext) for ext in ALLOWED_EXTENSIONS)

@router.post("/upload")
def upload_file(
    uploaded_file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    # Check user role
    if current_user.role != "ops":
        raise HTTPException(status_code=403, detail="Only Ops users can upload files")

    # Check file extension
    if not allowed_file(uploaded_file.filename):
        raise HTTPException(status_code=400, detail="Invalid file type. Allowed: .docx, .pptx, .xlsx")

    # Save the file
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(uploaded_file.file, buffer)

    # Store in DB
    new_file = models.File(filename=uploaded_file.filename, uploader_id=current_user.id)
    db.add(new_file)
    db.commit()
    db.refresh(new_file)

    return {"message": "File uploaded successfully", "file_id": new_file.id}
