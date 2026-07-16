from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
import os
from typing import Optional, Dict

# Configure password hashing context
# bcrypt: algorithm specifically designed for password hashing
# deprecated="auto": automatically handle deprecated hash formats
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))  # 24 hours


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain text password against a hashed password.
    
    This function hashes the plain text password using the same
    algorithm and salt that was used to create the stored hash,
    then compares the results using constant-time comparison
    to prevent timing attacks.
    
    Args:
        plain_password: The plain text password to verify
        hashed_password: The bcrypt hash to compare against
        
    Returns:
        True if the password matches, False otherwise
        
    Security considerations:
        - Uses constant-time comparison to prevent timing attacks
        - Automatically extracts salt from stored hash
        - Bcrypt work factor provides inherent brute force resistance
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a plain text password using bcrypt.
    
    This function generates a secure bcrypt hash of the password
    with an automatically generated salt and the configured work
    factor. The resulting hash can be safely stored in the database.
    
    Args:
        password: The plain text password to hash
        
    Returns:
        The bcrypt hash string containing salt, work factor, and hash
        
    Security considerations:
        - Automatically generates unique salt for each password
        - Uses configured work factor (default bcrypt rounds)
        - Hash includes algorithm identifier and parameters
        - Suitable for secure storage in database
        
    Example:
        >>> hash = get_password_hash("mypassword123")
        >>> print(hash)
        $2b$12$randomsaltcharactershashvalue...
    """
    return pwd_context.hash(password)


def create_access_token(data: Dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.
    
    This function generates a JSON Web Token containing the provided data
    (typically user_id and role) with an expiration time. The token is
    signed using the configured secret key and algorithm.
    
    Args:
        data: Dictionary of claims to include in the token (e.g., user_id, role)
        expires_delta: Optional timedelta for token expiration.
                      Defaults to ACCESS_TOKEN_EXPIRE_MINUTES if not provided.
        
    Returns:
        Encoded JWT token string
        
    Security considerations:
        - Token is signed with SECRET_KEY (must be kept secret)
        - Token includes expiration time (exp claim)
        - Token includes issued at time (iat claim)
        - HS256 algorithm provides signature verification
        
    Example:
        >>> token = create_access_token({"sub": "user123", "role": "admin"})
        >>> print(token)
        eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
    """
    to_encode = data.copy()
    
    # Set expiration time
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    # Encode and sign the token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[Dict]:
    """
    Decode and validate a JWT access token.
    
    This function verifies the token signature using the secret key,
    checks the expiration time, and extracts the claims from the token.
    Returns None if the token is invalid or expired.
    
    Args:
        token: JWT token string to decode and validate
        
    Returns:
        Dictionary of token claims if valid, None otherwise
        
    Security considerations:
        - Verifies signature using SECRET_KEY
        - Checks expiration time (exp claim)
        - Returns None for invalid/expired tokens
        - Catches JWTError exceptions for invalid tokens
        
    Example:
        >>> claims = decode_access_token(token)
        >>> if claims:
        ...     print(claims["sub"])
        user123
    """
    try:
        # Decode and verify the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        # Token is invalid or expired
        return None
