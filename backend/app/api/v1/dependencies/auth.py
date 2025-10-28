from typing import Annotated, List, Optional, Tuple

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.api.v1.schemas.token import TokenPayload
from app.core.config import settings
from app.core.security import ALGORITHM, validate_access_token
from app.db.session import get_db
from app.models.user import User, UserRole
from app.services import user_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    # Validate the token
    is_valid, payload = validate_access_token(token)
    
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    
    try:
        # Extract user ID from payload
        user_id = int(payload.get("sub"))
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )
    
    # Get user from database
    user = user_service.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Inactive user"
        )
    
    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user


def check_role_permission(
    required_roles: List[UserRole],
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.role not in required_roles:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user


def get_admin_permission(current_user: User = Depends(get_current_user)) -> User:
    return check_role_permission([UserRole.ADMIN], current_user)


def get_department_head_permission(current_user: User = Depends(get_current_user)) -> User:
    return check_role_permission([UserRole.ADMIN, UserRole.DEPARTMENT_HEAD], current_user)


def get_analyst_permission(current_user: User = Depends(get_current_user)) -> User:
    return check_role_permission([UserRole.ADMIN, UserRole.DEPARTMENT_HEAD, UserRole.ANALYST], current_user)