"""User data model for OAuth authentication and storage."""
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List


class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    full_name: str
    picture_url: Optional[str] = None
    provider: str  # 'google' or 'discord'
    provider_id: str  # User ID from OAuth provider


class UserCreate(UserBase):
    """Schema for creating a new user."""
    pass


class UserResponse(UserBase):
    """Schema for user API responses (no sensitive data)."""
    user_id: str
    created_at: datetime
    last_login: datetime
    is_active: bool


class UserDB(UserBase):
    """Complete user document for MongoDB storage."""
    user_id: str  # Unique identifier
    password_hash: Optional[str] = None  # For future local auth
    access_token: Optional[str] = None  # Cached OAuth token
    refresh_token: Optional[str] = None  # Cached refresh token
    token_expiry: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    last_login: datetime
    is_active: bool = True
    login_count: int = 0
    providers: List[dict] = []  # Multiple OAuth providers per user
    metadata: dict = {}  # Flexible field for additional user data


class TokenResponse(BaseModel):
    """JWT token response."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse
