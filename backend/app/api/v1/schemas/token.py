from typing import Optional, Dict, Any

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class RefreshToken(BaseModel):
    refresh_token: str


class TokenPayload(BaseModel):
    sub: Optional[int] = None
    type: Optional[str] = None
    exp: Optional[int] = None
    iat: Optional[int] = None