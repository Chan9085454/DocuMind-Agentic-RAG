from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
import hashlib

SECRET_KEY = "2bc289e4a6fdfe738046ae6193245404a462efc144dd43a134614e996f56e231"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["pbkdf2_sha256", "bcrypt_sha256", "bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def hash_password(password: str) -> str:
    # pre-hash with SHA-256 to avoid any backend limits
    pw = password if isinstance(password, str) else str(password)
    pre = hashlib.sha256(pw.encode("utf-8")).hexdigest()
    return pwd_context.hash(pre)


def verify_password(password: str, hashed: str) -> bool:
    pw = password if isinstance(password, str) else str(password)
    pre = hashlib.sha256(pw.encode("utf-8")).hexdigest()
    try:
        if pwd_context.verify(pre, hashed):
            return True
    except Exception:
        pass

    try:
        if pwd_context.verify(password, hashed):
            return True
    except Exception:
        pass

    return False


def create_access_token(data: dict, expires_minutes: int = 60):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return username

    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")