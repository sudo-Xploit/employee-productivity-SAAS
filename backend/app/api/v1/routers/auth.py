from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.v1.schemas.token import Token, TokenPair, RefreshToken
from app.api.v1.schemas.user import User, UserCreate
from app.core.config import settings
from app.core.security import create_access_token, create_refresh_token, validate_refresh_token, create_token_pair
from app.db.session import get_db
from app.services import user_service
from app.api.v1.dependencies.auth import get_current_user

router = APIRouter()


@router.post("/register", response_model=User)
def register(*, db: Session = Depends(get_db), user_in: UserCreate) -> Any:
    """Register a new user."""
    user = user_service.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this email already exists in the system.",
        )
    user = user_service.create(db, obj_in=user_in)
    return user


@router.post("/login", response_model=TokenPair)
def login(*, db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    """OAuth2 compatible token login, get an access token and refresh token for future requests."""
    user = user_service.authenticate(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    elif not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    
    # Create both access and refresh tokens
    return create_token_pair(user.id)


@router.post("/refresh", response_model=TokenPair)
def refresh_token(*, db: Session = Depends(get_db), refresh_token_in: RefreshToken) -> Any:
    """Refresh access token using a valid refresh token."""
    is_valid, payload = validate_refresh_token(refresh_token_in.refresh_token)
    
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )
    
    # Get user from token payload
    user_id = int(payload.get("sub"))
    user = user_service.get(db, id=user_id)
    
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )
    
    # Create new token pair
    return create_token_pair(user.id)


@router.get("/me", response_model=User)
def read_users_me(current_user: User = Depends(get_current_user)) -> Any:
    """Get current user."""
    return current_user