from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.orm import declared_attr
from backend.database import Base


class BaseModel(Base):
    """
    Base model class for all database models.
    
    This class provides common attributes and functionality
    that are shared across all database tables:
    - id: Primary key
    - created_at: Timestamp for record creation
    - updated_at: Timestamp for last modification
    
    All models should inherit from this class to ensure
    consistent structure and automatic timestamp management.
    """
    
    __abstract__ = True
    
    @declared_attr
    def __tablename__(cls):
        """
        Automatically generate table name from class name.
        
        Converts CamelCase class names to snake_case table names.
        Example: FlightSession -> flight_session
        """
        return cls.__name__.lower()
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    """Primary key for the table."""
    
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    """Timestamp when the record was created."""
    
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    """Timestamp when the record was last updated."""
    
    def __repr__(self):
        """String representation of the model."""
        return f"<{self.__class__.__name__}(id={self.id})>"
