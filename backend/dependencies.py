from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional
from backend.core.security import decode_access_token
from backend.database import get_db
from backend.models.user import User, UserRole

# HTTP Bearer token scheme for JWT authentication
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency to get the current authenticated user from JWT token.
    
    This function:
    1. Extracts the JWT token from the Authorization header
    2. Decodes and validates the token
    3. Retrieves the user from the database
    4. Returns the user object if authentication succeeds
    
    Args:
        credentials: HTTP Bearer credentials containing JWT token
        db: Database session dependency
        
    Returns:
        User object representing the authenticated user
        
    Raises:
        HTTPException: If token is invalid, expired, or user not found
        
    Security considerations:
        - Token signature is verified using SECRET_KEY
        - Token expiration is checked
        - User existence is verified in database
        - Returns 401 for authentication failures
    """
    # Extract token from credentials
    token = credentials.credentials
    
    # Decode and validate token
    payload = decode_access_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Extract user ID from token
    user_id: Optional[int] = payload.get("user_id")
    
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token does not contain user_id",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Retrieve user from database
    user = db.query(User).filter(User.id == user_id).first()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


def get_current_admin(current_user: User = Depends(get_current_user)) -> User:
    """
    Dependency to verify the current user is an administrator.
    
    This function checks if the authenticated user has the administrator role.
    It is used to protect administrative endpoints.
    
    Args:
        current_user: Current authenticated user from get_current_user dependency
        
    Returns:
        User object representing the authenticated administrator
        
    Raises:
        HTTPException: If user is not an administrator (403 Forbidden)
        
    Security considerations:
        - Enforces role-based access control (RBAC)
        - Only administrators can access protected endpoints
        - Returns 403 for authorization failures
    """
    if not current_user.is_administrator():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized. Administrator access required."
        )
    
    return current_user


def get_current_maintenance_engineer(current_user: User = Depends(get_current_user)) -> User:
    """
    Dependency to verify the current user is a maintenance engineer.
    
    This function checks if the authenticated user has the maintenance engineer role.
    It is used to protect maintenance-specific endpoints.
    
    Args:
        current_user: Current authenticated user from get_current_user dependency
        
    Returns:
        User object representing the authenticated maintenance engineer
        
    Raises:
        HTTPException: If user is not a maintenance engineer (403 Forbidden)
    """
    if not current_user.is_maintenance_engineer():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized. Maintenance Engineer access required."
        )
    
    return current_user


def get_current_drone_operator(current_user: User = Depends(get_current_user)) -> User:
    """
    Dependency to verify the current user is a drone operator.
    
    This function checks if the authenticated user has the drone operator role.
    It is used to protect operator-specific endpoints.
    
    Args:
        current_user: Current authenticated user from get_current_user dependency
        
    Returns:
        User object representing the authenticated drone operator
        
    Raises:
        HTTPException: If user is not a drone operator (403 Forbidden)
    """
    if not current_user.is_drone_operator():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized. Drone Operator access required."
        )
    
    return current_user


def require_role(required_role: UserRole):
    """
    Factory function to create a role-based dependency.
    
    This function returns a dependency that checks if the current user
    has the specified role. It provides a flexible way to enforce
    role-based access control for any role.
    
    Args:
        required_role: The UserRole enum value required for access
        
    Returns:
        Dependency function that checks the user's role
        
    Example:
        @router.get("/admin-only")
        def admin_endpoint(user: User = Depends(require_role(UserRole.ADMINISTRATOR))):
            return {"message": "Welcome admin"}
    """
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Not authorized. {required_role.value.replace('_', ' ').title()} access required."
            )
        return current_user
    
    return role_checker
