"""
Reset Administrator Password Script

This script resets the administrator account password to a known value.
Use this if you have forgotten the admin password or need to reset it.
"""

from backend.database import SessionLocal
from backend.models.user import User
from backend.core.security import get_password_hash

def reset_admin_password(new_password: str = "Admin123!"):
    """
    Reset the administrator account password.
    
    Args:
        new_password: The new password to set (default: Admin123!)
    """
    db = SessionLocal()
    
    try:
        # Find the admin user
        admin = db.query(User).filter(User.username == 'admin').first()
        
        if not admin:
            print("ERROR: Admin account not found!")
            print("Please create an admin account first.")
            return False
        
        # Hash the new password
        hashed_password = get_password_hash(new_password)
        
        # Update the password
        admin.hashed_password = hashed_password
        db.commit()
        
        print(f"SUCCESS: Admin password has been reset!")
        print(f"Username: {admin.username}")
        print(f"Email: {admin.email}")
        print(f"Role: {admin.role}")
        print(f"New password: {new_password}")
        print(f"\nYou can now log in with:")
        print(f"  Username: admin")
        print(f"  Password: {new_password}")
        
        return True
        
    except Exception as e:
        print(f"ERROR: Failed to reset password: {e}")
        db.rollback()
        return False
        
    finally:
        db.close()

if __name__ == "__main__":
    import sys
    
    # Allow custom password from command line
    password = sys.argv[1] if len(sys.argv) > 1 else "Admin123!"
    
    print("=" * 60)
    print("Administrator Password Reset")
    print("=" * 60)
    print()
    
    reset_admin_password(password)
