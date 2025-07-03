# app/main.py

from fastapi import FastAPI
from app.routes import ops, client
from app.database import Base, engine
import os

# Ensure uploads folder exists
if not os.path.exists("uploads"):
    os.makedirs("uploads")

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Secure File Sharing System")

app.include_router(ops.router, prefix="/ops", tags=["Ops"])
app.include_router(client.router, prefix="/client", tags=["Client"])
