# app/main.py

import os
from fastapi import FastAPI
import uvicorn

from app.database import Base, engine
from app.routes.client import router as client_user
from app.routes.ops import router as ops_user


# Initialize app
app = FastAPI(title="Secure File Sharing System")

# Health check route
@app.get("/")
def root():
    return {"message": "Secure File Sharing API is running!"}

# Include routers
app.include_router(client_user, prefix="/client", tags=["Client User"])
app.include_router(ops_user, prefix="/ops", tags=["Ops User"])


# Ensure 'uploads' directory exists
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# Create tables
Base.metadata.create_all(bind=engine)

# For local testing (not used on Render)
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=10000)
