# app/utils.py

from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from app.config import settings
from app.config import settings
print("TOKEN GENERATION SECRET_KEY:", settings.SECRET_KEY)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
fernet = Fernet(settings.ENCRYPTION_KEY)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict, expires_delta: int = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta or settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def encrypt_url(data: str) -> str:
    return fernet.encrypt(data.encode()).decode()

def decrypt_url(token: str) -> str:
    return fernet.decrypt(token.encode()).decode()
