from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.schemas.auth import Token
from backend.services.auth_service import AuthService

router = APIRouter()


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Authenticate user and return access token.
    
    This endpoint implements OAuth2 password flow for user authentication.
    It validates the provided username and password, and if valid,
    returns a JWT access token that can be used for subsequent requests.
    
    Args:
        form_data: OAuth2 form containing username and password
        db: Database session dependency
        
    Returns:
        Token object containing access token and token type
        
    Raises:
        HTTPException: If authentication fails (401 Unauthorized)
        
    Security considerations:
        - Uses OAuth2PasswordRequestForm for standard OAuth2 flow
        - Password verification uses constant-time comparison
        - Returns generic error message (no information leak)
        - Token expires after 24 hours
        - Token includes user role for authorization
        
    Example request:
        POST /api/v1/auth/login
        Content-Type: application/x-www-form-urlencoded
        username=admin&password=secret123
        
    Example response:
        {
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "token_type": "bearer"
        }
    """
    # Authenticate user credentials
    user = AuthService.authenticate_user(db, form_data.username, form_data.password)
    
    # Return 401 if authentication fails
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Generate and return access token
    token = AuthService.create_token_for_user(user)
    return token
