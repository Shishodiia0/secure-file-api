# app/routes/client.py

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app import schemas, models, utils, auth
from app.database import get_db
from app.config import settings
import shutil
import os

router = APIRouter()

UPLOAD_FOLDER = "uploads"

# 1. SIGN UP
@router.post("/signup")
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = utils.hash_password(user.password)
    new_user = models.User(email=user.email, hashed_password=hashed, role="client")
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    encrypted = utils.encrypt_url(user.email)
    return {
        "message": "Signup successful. Please verify your email.",
        "verification_url": f"/client/email-verify/{encrypted}"
    }

# 2. EMAIL VERIFY (Mocked)
@router.get("/email-verify/{token}")
def verify_email(token: str, db: Session = Depends(get_db)):
    try:
        email = utils.decrypt_url(token)
    except:
        raise HTTPException(status_code=400, detail="Invalid verification token")

    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_verified = True
    db.commit()
    return {"message": "Email verified successfully"}

# 3. LOGIN
@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not utils.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect credentials")

    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Email not verified")

    access_token = utils.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# 4. LIST ALL FILES
@router.get("/files")
def list_files(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    if current_user.role != "client":
        raise HTTPException(status_code=403, detail="Only client can access this")

    files = db.query(models.File).all()
    return [{"id": f.id, "name": f.filename} for f in files]

# 5. GET ENCRYPTED DOWNLOAD LINK
@router.get("/download/{file_id}")
def generate_download_link(file_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    if current_user.role != "client":
        raise HTTPException(status_code=403)

    file = db.query(models.File).filter(models.File.id == file_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    encrypted = utils.encrypt_url(str(file_id))
    return {
        "download-link": f"/client/download-file/{encrypted}",
        "message": "success"
    }

# 6. ACTUAL DOWNLOAD FILE
@router.get("/download-file/{enc}")
def download_file(enc: str, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    if current_user.role != "client":
        raise HTTPException(status_code=403)

    try:
        file_id = int(utils.decrypt_url(enc))
    except:
        raise HTTPException(status_code=400, detail="Invalid encrypted link")

    file = db.query(models.File).filter(models.File.id == file_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not on server")

    return {
        "filename": file.filename,
        "message": "Download allowed (mocked). Serve file via static file or stream."
    }
# Only for development/testing — remove later

# @router.post("/ops-temp-signup")
# def create_ops_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     existing = db.query(models.User).filter(models.User.email == user.email).first()
#     if existing:
#         raise HTTPException(status_code=400, detail="Email already registered")

#     hashed = utils.hash_password(user.password)
#     new_user = models.User(
#         email=user.email,
#         hashed_password=hashed,
#         role="ops",        # 🚀 key difference here
#         is_verified=True   # skip email verify for quick testing
#     )
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return {"message": "Ops user created"}
