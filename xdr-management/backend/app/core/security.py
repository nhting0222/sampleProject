from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from enum import Enum

from .config import settings


# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


class UserRole(str, Enum):
    ADMIN = "admin"
    ANALYST = "analyst"
    VIEWER = "viewer"


class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[UserRole] = None


class Token(BaseModel):
    access_token: str
    token_type: str
    user: dict


class UserBase(BaseModel):
    username: str
    email: str
    full_name: str
    role: UserRole


class UserCreate(UserBase):
    password: str


class UserInDB(UserBase):
    id: str
    hashed_password: str
    is_active: bool = True
    created_at: str


class UserResponse(UserBase):
    id: str
    is_active: bool


# Mock user database (will be replaced with real DB later)
users_db = {
    "admin": {
        "id": "USR-001",
        "username": "admin",
        "email": "admin@xdr.local",
        "full_name": "System Administrator",
        "hashed_password": pwd_context.hash("admin123"),
        "role": UserRole.ADMIN,
        "is_active": True,
        "created_at": "2026-01-01T00:00:00Z"
    },
    "analyst": {
        "id": "USR-002",
        "username": "analyst",
        "email": "analyst@xdr.local",
        "full_name": "Security Analyst",
        "hashed_password": pwd_context.hash("analyst123"),
        "role": UserRole.ANALYST,
        "is_active": True,
        "created_at": "2026-01-01T00:00:00Z"
    },
    "viewer": {
        "id": "USR-003",
        "username": "viewer",
        "email": "viewer@xdr.local",
        "full_name": "Security Viewer",
        "hashed_password": pwd_context.hash("viewer123"),
        "role": UserRole.VIEWER,
        "is_active": True,
        "created_at": "2026-01-01T00:00:00Z"
    }
}


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def get_user(username: str) -> Optional[dict]:
    if username in users_db:
        return users_db[username]
    return None


def authenticate_user(username: str, password: str) -> Optional[dict]:
    user = get_user(username)
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        role = payload.get("role")
        token_data = TokenData(username=username, role=role)
    except JWTError:
        raise credentials_exception

    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: dict = Depends(get_current_user)) -> dict:
    if not current_user.get("is_active"):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


# Role-based access control decorators
def require_role(allowed_roles: list[UserRole]):
    async def role_checker(current_user: dict = Depends(get_current_active_user)) -> dict:
        if current_user["role"] not in [r.value for r in allowed_roles]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user
    return role_checker


# Convenience dependencies
require_admin = require_role([UserRole.ADMIN])
require_analyst = require_role([UserRole.ADMIN, UserRole.ANALYST])
require_viewer = require_role([UserRole.ADMIN, UserRole.ANALYST, UserRole.VIEWER])
