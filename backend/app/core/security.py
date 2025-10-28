from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Tuple, Union

from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import ValidationError

from app.core.config import settings

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"
ALGORITHM = "HS256"


def create_access_token(
    subject: Union[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """Create a new access token"""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode = {
        "exp": expire, 
        "iat": datetime.utcnow(),
        "sub": str(subject), 
        "type": ACCESS_TOKEN_TYPE
    }
    
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(
    subject: Union[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """Create a new refresh token"""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )
    
    to_encode = {
        "exp": expire, 
        "iat": datetime.utcnow(),
        "sub": str(subject), 
        "type": REFRESH_TOKEN_TYPE
    }
    
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> Dict[str, Any]:
    """Decode and validate a token"""
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[ALGORITHM]
        )
        return payload
    except (JWTError, ValidationError):
        return {}


def validate_access_token(token: str) -> Tuple[bool, Dict[str, Any]]:
    """Validate an access token and return the payload if valid"""
    payload = decode_token(token)
    
    if not payload:
        return False, {}
    
    # Check if token is an access token
    if payload.get("type") != ACCESS_TOKEN_TYPE:
        return False, {}
    
    # Check if token has expired
    expiration = datetime.fromtimestamp(payload.get("exp", 0))
    if expiration < datetime.utcnow():
        return False, {}
    
    return True, payload


def validate_refresh_token(token: str) -> Tuple[bool, Dict[str, Any]]:
    """Validate a refresh token and return the payload if valid"""
    payload = decode_token(token)
    
    if not payload:
        return False, {}
    
    # Check if token is a refresh token
    if payload.get("type") != REFRESH_TOKEN_TYPE:
        return False, {}
    
    # Check if token has expired
    expiration = datetime.fromtimestamp(payload.get("exp", 0))
    if expiration < datetime.utcnow():
        return False, {}
    
    return True, payload


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash"""
    return password_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password for storing"""
    return password_context.hash(password)


def create_token_pair(subject: Union[str, Any]) -> Dict[str, str]:
    """Create both access and refresh tokens"""
    access_token = create_access_token(subject)
    refresh_token = create_refresh_token(subject)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }