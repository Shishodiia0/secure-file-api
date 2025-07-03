# app/main.py

from fastapi import FastAPI
from app.routes import ops, client
from app.database import Base, engine
import os
import uvicorn
from fastapi import FastAPI
from app.routes import client_user, ops_user, file_access

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Secure File Sharing API is running!"}

app.include_router(client_user.router)
app.include_router(ops_user.router)
app.include_router(file_access.router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=10000, reload=False)

# Ensure uploads folder exists
if not os.path.exists("uploads"):
    os.makedirs("uploads")

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Secure File Sharing System")

app.include_router(ops.router, prefix="/ops", tags=["Ops"])
app.include_router(client.router, prefix="/client", tags=["Client"])
