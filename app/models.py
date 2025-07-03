# app/models.py

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_verified = Column(Boolean, default=False)
    role = Column(String, nullable=False)  # "ops" or "client"
    files = relationship("File", back_populates="uploader")

class File(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    uploader_id = Column(Integer, ForeignKey("users.id"))
    uploader = relationship("User", back_populates="files")
