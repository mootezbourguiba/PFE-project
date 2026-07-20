from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db
from backend.crud.user import crud_user
from backend.schemas.user import UserCreate, UserUpdate, UserResponse, UserDisable, UserStatusResponse
from backend.dependencies import get_current_admin, get_current_user
from backend.models.user import User

router = APIRouter()


@router.get("/", response_model=List[UserResponse])
def get_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Get list of all users (Administrator only).
    
    This endpoint retrieves all users from the database with pagination.
    Only administrators can access this endpoint.
    
    Args:
        skip: Number of records to skip (pagination)
        limit: Maximum number of records to return
        current_user: Current authenticated administrator (from dependency)
        db: Database session
        
    Returns:
        List of UserResponse objects containing user information
        
    Raises:
        HTTPException: 403 if user is not an administrator
        
    Security considerations:
        - Requires JWT authentication
        - Restricted to administrators only
        - Excludes sensitive data (passwords)
    """
    users = crud_user.get_users(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user: UserCreate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Create a new user (Administrator only).
    
    This endpoint creates a new user with the provided credentials.
    The password is automatically hashed before storage. Only administrators
    can create new users.
    
    Args:
        user: UserCreate schema containing username, email, password, and role
        current_user: Current authenticated administrator (from dependency)
        db: Database session
        
    Returns:
        UserResponse object containing the created user information
        
    Raises:
        HTTPException: 403 if user is not an administrator
        HTTPException: 400 if username or email already exists
        
    Security considerations:
        - Requires JWT authentication
        - Restricted to administrators only
        - Password is hashed using bcrypt before storage
        - Unique constraints enforced on username and email
    """
    # Check if username already exists
    existing_user = crud_user.get_user_by_username(db, username=user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    
    # Check if email already exists
    existing_email = crud_user.get_user_by_email(db, email=user.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )
    
    # Create user
    db_user = crud_user.create_user(
        db=db,
        username=user.username,
        email=user.email,
        password=user.password,
        role=user.role
    )
    db.commit()
    db.refresh(db_user)
    
    return db_user


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Get a specific user by ID (Administrator only).
    
    This endpoint retrieves a specific user by their ID.
    Only administrators can access this endpoint.
    
    Args:
        user_id: ID of the user to retrieve
        current_user: Current authenticated administrator (from dependency)
        db: Database session
        
    Returns:
        UserResponse object containing user information
        
    Raises:
        HTTPException: 403 if user is not an administrator
        HTTPException: 404 if user not found
        
    Security considerations:
        - Requires JWT authentication
        - Restricted to administrators only
        - Excludes sensitive data (passwords)
    """
    user = crud_user.get_user_by_id(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Update a user's information (Administrator only).
    
    This endpoint updates a user's email and/or role.
    Only administrators can update user information.
    
    Args:
        user_id: ID of the user to update
        user_update: UserUpdate schema containing fields to update
        current_user: Current authenticated administrator (from dependency)
        db: Database session
        
    Returns:
        UserResponse object containing updated user information
        
    Raises:
        HTTPException: 403 if user is not an administrator
        HTTPException: 404 if user not found
        HTTPException: 400 if email already exists (when updating email)
        
    Security considerations:
        - Requires JWT authentication
        - Restricted to administrators only
        - Email uniqueness is enforced
        - Cannot update password through this endpoint
    """
    # Check if user exists
    db_user = crud_user.get_user_by_id(db, user_id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # If updating email, check if new email already exists
    if user_update.email:
        existing_email = crud_user.get_user_by_email(db, email=user_update.email)
        if existing_email and existing_email.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )
    
    # Update user
    updated_user = crud_user.update_user(
        db=db,
        user_id=user_id,
        email=user_update.email,
        role=user_update.role
    )
    db.commit()
    db.refresh(updated_user)
    
    return updated_user


@router.patch("/{user_id}/disable", response_model=UserStatusResponse)
def disable_user(
    user_id: int,
    user_disable: UserDisable,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Disable or enable a user account (Administrator only).
    
    This endpoint allows administrators to disable user accounts without
    permanently deleting them. This is appropriate for aircraft maintenance
    platforms where user history must be preserved.
    
    Args:
        user_id: ID of the user to disable/enable
        user_disable: UserDisable schema containing disabled flag and reason
        current_user: Current authenticated administrator (from dependency)
        db: Database session
        
    Returns:
        UserStatusResponse object containing user status
        
    Raises:
        HTTPException: 403 if user is not an administrator
        HTTPException: 404 if user not found
        HTTPException: 400 if trying to disable self
        
    Security considerations:
        - Requires JWT authentication
        - Restricted to administrators only
        - Cannot disable own account
        - Preserves user history and data
    """
    # Check if user exists
    db_user = crud_user.get_user_by_id(db, user_id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Prevent administrator from disabling themselves
    if db_user.id == current_user.id and user_disable.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot disable your own account"
        )
    
    # Update user with disabled status
    updated_user = crud_user.update_user(
        db=db,
        user_id=user_id,
        disabled=user_disable.disabled,
        disabled_reason=user_disable.reason if user_disable.disabled else None
    )
    db.commit()
    db.refresh(updated_user)
    
    return UserStatusResponse(
        id=updated_user.id,
        username=updated_user.username,
        disabled=updated_user.disabled,
        reason=updated_user.disabled_reason
    )


@router.patch("/{user_id}/enable", response_model=UserStatusResponse)
def enable_user(
    user_id: int,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Enable a disabled user account (Administrator only).
    
    This endpoint allows administrators to re-enable previously disabled
    user accounts.
    
    Args:
        user_id: ID of the user to enable
        current_user: Current authenticated administrator (from dependency)
        db: Database session
        
    Returns:
        UserStatusResponse object containing user status
        
    Raises:
        HTTPException: 403 if user is not an administrator
        HTTPException: 404 if user not found
        
    Security considerations:
        - Requires JWT authentication
        - Restricted to administrators only
        - Preserves user history and data
    """
    # Check if user exists
    db_user = crud_user.get_user_by_id(db, user_id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Enable user by setting disabled to False and clearing reason
    updated_user = crud_user.update_user(
        db=db,
        user_id=user_id,
        disabled=False,
        disabled_reason=None
    )
    db.commit()
    db.refresh(updated_user)
    
    return UserStatusResponse(
        id=updated_user.id,
        username=updated_user.username,
        disabled=updated_user.disabled,
        reason=updated_user.disabled_reason
    )
