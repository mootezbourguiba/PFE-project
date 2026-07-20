from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """
    Base schema for user data.
    
    This schema contains common fields shared across multiple user schemas.
    It provides a foundation for request/response validation.
    
    Attributes:
        username: Unique username for login
        email: Unique email address
    """
    username: str = Field(..., min_length=3, max_length=50, description="Unique username")
    email: EmailStr = Field(..., description="Unique email address")


class UserCreate(UserBase):
    """
    Schema for creating a new user.
    
    This schema is used for POST /users/ requests to create new users.
    It includes password which is required for user creation.
    
    Attributes:
        username: Unique username
        email: Unique email address
        password: Plain text password (will be hashed before storage)
        role: User role (default: maintenance_engineer)
    """
    password: str = Field(..., min_length=8, description="Password (min 8 characters)")
    role: str = Field(
        default="maintenance_engineer",
        description="User role: administrator, maintenance_engineer, or drone_operator"
    )


class UserUpdate(BaseModel):
    """
    Schema for updating user information.
    
    This schema is used for PUT /users/{id} requests to update user data.
    All fields are optional - only provided fields will be updated.
    
    Attributes:
        email: New email address (optional)
        role: New role (optional)
    """
    email: Optional[EmailStr] = Field(None, description="New email address")
    role: Optional[str] = Field(
        None,
        description="New role: administrator, maintenance_engineer, or drone_operator"
    )


class UserResponse(UserBase):
    """
    Schema for user response data.
    
    This schema is used for API responses containing user information.
    It excludes sensitive data like passwords.
    
    Attributes:
        id: User ID
        username: Username
        email: Email address
        role: User role
        created_at: Account creation timestamp
        updated_at: Last update timestamp
    """
    id: int
    role: str
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic configuration for ORM mode."""
        from_attributes = True


class UserDisable(BaseModel):
    """
    Schema for disabling a user.
    
    This schema is used for PATCH /users/{id}/disable requests.
    It allows administrators to disable user accounts without deletion.
    
    Attributes:
        disabled: Boolean flag to disable/enable user
        reason: Optional reason for disabling the user
    """
    disabled: bool = Field(..., description="Disable or enable user account")
    reason: Optional[str] = Field(None, description="Reason for disabling the user")


class UserStatusResponse(BaseModel):
    """
    Schema for user status response.
    
    This schema is used for responses to disable/enable operations.
    
    Attributes:
        id: User ID
        username: Username
        disabled: Disabled status
        reason: Reason for disabling (if any)
    """
    id: int
    username: str
    disabled: bool
    reason: Optional[str] = None

    class Config:
        """Pydantic configuration for ORM mode."""
        from_attributes = True
