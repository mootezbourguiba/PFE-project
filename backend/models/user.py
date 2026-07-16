from sqlalchemy import Column, String, Enum as SQLEnum
from sqlalchemy.orm import relationship
import enum
from backend.models.base import BaseModel


class UserRole(str, enum.Enum):
    """Enumeration of user roles for role-based access control."""
    
    ADMINISTRATOR = "administrator"
    """Full system access including user management."""
    
    MAINTENANCE_ENGINEER = "maintenance_engineer"
    """Access to monitoring, historical data, and anomaly analysis."""
    
    DRONE_OPERATOR = "drone_operator"
    """Access to real-time alerts and basic status only."""


class User(BaseModel):
    """
    User model representing system users.
    
    This model stores user authentication credentials and role information
    for implementing role-based access control (RBAC). Each user can
    create multiple flight sessions.
    
    Attributes:
        username: Unique username for login
        email: Unique email address for contact and login
        hashed_password: Bcrypt hash of user password (never plain text)
        role: User role determining access permissions
        flight_sessions: Relationship to user's flight sessions
    """
    
    username = Column(String(50), unique=True, nullable=False, index=True)
    """Unique username for login identification."""
    
    email = Column(String(100), unique=True, nullable=False, index=True)
    """Unique email address for contact and login."""
    
    hashed_password = Column(String(255), nullable=False)
    """Bcrypt hash of user password (never store plain text)."""
    
    role = Column(
        SQLEnum(UserRole),
        nullable=False,
        default=UserRole.MAINTENANCE_ENGINEER
    )
    """User role determining access permissions."""
    
    # Relationship to FlightSession
    flight_sessions = relationship(
        "FlightSession",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    """One-to-many relationship with FlightSession."""
    
    def __repr__(self):
        """String representation of the user."""
        return f"<User(id={self.id}, username='{self.username}', role='{self.role}')>"
    
    def has_role(self, role: UserRole) -> bool:
        """
        Check if user has a specific role.
        
        Args:
            role: Role to check against
            
        Returns:
            True if user has the specified role, False otherwise
        """
        return self.role == role
    
    def is_administrator(self) -> bool:
        """Check if user is an administrator."""
        return self.role == UserRole.ADMINISTRATOR
    
    def is_maintenance_engineer(self) -> bool:
        """Check if user is a maintenance engineer."""
        return self.role == UserRole.MAINTENANCE_ENGINEER
    
    def is_drone_operator(self) -> bool:
        """Check if user is a drone operator."""
        return self.role == UserRole.DRONE_OPERATOR
