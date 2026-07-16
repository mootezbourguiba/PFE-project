from sqlalchemy.orm import Session
from backend.models.user import User
from backend.core.security import verify_password, create_access_token
from backend.schemas.auth import Token
from typing import Optional


class AuthService:
    """
    Service layer for authentication business logic.
    
    This service handles the business logic for user authentication,
    including credential verification and token generation. It
    separates business logic from API endpoints and CRUD operations.
    """
    
    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
        """
        Authenticate a user by username and password.
        
        This function retrieves the user from the database and verifies
        the provided password against the stored hash. Returns the user
        object if authentication succeeds, None otherwise.
        
        Args:
            db: Database session
            username: Username to authenticate
            password: Plain text password to verify
            
        Returns:
            User object if authentication succeeds, None otherwise
            
        Security considerations:
            - Password verification uses constant-time comparison
            - Returns None for invalid credentials (no information leak)
            - Does not reveal whether username exists (prevents enumeration)
        """
        user = db.query(User).filter(User.username == username).first()
        
        # Check if user exists and password is correct
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
            
        return user
    
    @staticmethod
    def create_token_for_user(user: User) -> Token:
        """
        Create a JWT access token for a user.
        
        This function generates a JWT token containing the user's ID,
        username, and role. The token is valid for 24 hours by default.
        
        Args:
            user: User object to generate token for
            
        Returns:
            Token object containing access token and token type
            
        Security considerations:
            - Token includes user_id for database queries
            - Token includes role for authorization
            - Token expires after configured time (24 hours)
            - Token is signed with SECRET_KEY
        """
        # Create token payload with user claims
        token_data = {
            "sub": user.username,
            "user_id": user.id,
            "role": user.role.value
        }
        
        # Generate access token
        access_token = create_access_token(token_data)
        
        # Return token response
        return Token(access_token=access_token, token_type="bearer")
