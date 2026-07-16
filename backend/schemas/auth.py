from pydantic import BaseModel
from typing import Optional


class LoginRequest(BaseModel):
    """
    Schema for user login request.
    
    This schema defines the expected input for the login endpoint.
    It validates that both username and password are provided.
    
    Attributes:
        username: User's unique username
        password: User's plain text password (will be hashed for verification)
    """
    username: str
    password: str


class Token(BaseModel):
    """
    Schema for authentication token response.
    
    This schema defines the response format for successful authentication.
    It follows the OAuth2 Bearer Token standard.
    
    Attributes:
        access_token: JWT access token for authenticated requests
        token_type: Token type (always "bearer" for OAuth2)
    """
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """
    Schema for decoded JWT token data.
    
    This schema represents the claims extracted from a valid JWT token.
    Used internally for token validation.
    
    Attributes:
        username: Username from token subject claim
        user_id: User ID from token custom claim
        role: User role from token custom claim
    """
    username: Optional[str] = None
    user_id: Optional[int] = None
    role: Optional[str] = None
