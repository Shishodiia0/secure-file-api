# app/config.py

from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY").encode()

settings = Settings()
