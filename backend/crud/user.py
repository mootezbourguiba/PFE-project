from sqlalchemy.orm import Session
from backend.models.user import User
from backend.core.security import get_password_hash
from typing import Optional


class CRUDUser:
    """
    CRUD operations for User model.
    
    This class provides Create, Read, Update, and Delete operations
    for the User table, following the CRUD pattern. It encapsulates
    all database access logic for user entities.
    """
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        """
        Retrieve a user by ID.
        
        Args:
            db: Database session
            user_id: User ID to retrieve
            
        Returns:
            User object if found, None otherwise
        """
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[User]:
        """
        Retrieve a user by username.
        
        Args:
            db: Database session
            username: Username to retrieve
            
        Returns:
            User object if found, None otherwise
        """
        return db.query(User).filter(User.username == username).first()
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """
        Retrieve a user by email.
        
        Args:
            db: Database session
            email: Email to retrieve
            
        Returns:
            User object if found, None otherwise
        """
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_users(db: Session, skip: int = 0, limit: int = 100):
        """
        Retrieve a list of users with pagination.
        
        Args:
            db: Database session
            skip: Number of records to skip (pagination)
            limit: Maximum number of records to return
            
        Returns:
            List of User objects
        """
        return db.query(User).offset(skip).limit(limit).all()
    
    @staticmethod
    def create_user(db: Session, username: str, email: str, password: str, role: str = "maintenance_engineer") -> User:
        """
        Create a new user.
        
        This function creates a new user with the provided credentials.
        The password is hashed before storage. The user is added to the
        database session but not committed (caller must commit).
        
        Args:
            db: Database session
            username: Unique username
            email: Unique email address
            password: Plain text password (will be hashed)
            role: User role (default: maintenance_engineer)
            
        Returns:
            Created User object
            
        Security considerations:
            - Password is hashed using bcrypt before storage
            - Role is validated against enum values
            - Unique constraints on username and email enforced by database
        """
        # Hash the password before storage
        hashed_password = get_password_hash(password)
        
        # Create user object
        db_user = User(
            username=username,
            email=email,
            hashed_password=hashed_password,
            role=role
        )
        
        # Add to session (caller must commit)
        db.add(db_user)
        db.flush()  # Get ID without committing
        
        return db_user
    
    @staticmethod
    def update_user(db: Session, user_id: int, **kwargs) -> Optional[User]:
        """
        Update a user's information.
        
        Args:
            db: Database session
            user_id: User ID to update
            **kwargs: Fields to update (email, role, etc.)
            
        Returns:
            Updated User object if found, None otherwise
        """
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            return None
        
        # Update provided fields
        for key, value in kwargs.items():
            if hasattr(db_user, key):
                setattr(db_user, key, value)
        
        db.flush()
        return db_user
    
    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        """
        Delete a user.
        
        Args:
            db: Database session
            user_id: User ID to delete
            
        Returns:
            True if deleted, False if not found
        """
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            return False
        
        db.delete(db_user)
        return True


# Create singleton instance
crud_user = CRUDUser()
