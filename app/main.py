from fastapi import FastAPI
from app.routes import ops, client, client_user, ops_user, file_access
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
app.include_router(client_user.router)
app.include_router(ops_user.router)
app.include_router(file_access.router)

# Ensure uploads folder exists
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# Create DB tables
Base.metadata.create_all(bind=engine)
