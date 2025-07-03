from fastapi import FastAPI
from app.routes import ops, client
from app.routes.client_user import router as client_user_router
from app.routes.ops_user import router as ops_user_router
from app.routes.file_access import router as file_access_router

from app.database import Base, engine
import os

# Initialize FastAPI app once
app = FastAPI(title="Secure File Sharing System")

# Root route for health check
@app.get("/")
def root():
    return {"message": "✅ Secure File Sharing API is running on Render!"}

# Include all route modules
app.include_router(ops.router, prefix="/ops", tags=["Ops (Legacy)"])
app.include_router(client.router, prefix="/client", tags=["Client (Legacy)"])
app.include_router(client_user_router, prefix="/client", tags=["Client"])
app.include_router(ops_user_router, prefix="/ops", tags=["Ops"])
app.include_router(file_access_router, prefix="/files", tags=["Files"])


# Ensure uploads folder exists
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# Create DB tables
Base.metadata.create_all(bind=engine)
