"""
Fix Administrator Email Script

This script fixes the administrator account email to a valid format.
The .local TLD is reserved and causes FastAPI email validation to fail.
"""

from backend.database import SessionLocal
from backend.models.user import User

def fix_admin_email(new_email: str = "admin@avionav.com"):
    """
    Fix the administrator account email to a valid format.
    
    Args:
        new_email: The new valid email address (default: admin@avionav.com)
    """
    db = SessionLocal()
    
    try:
        # Find the admin user
        admin = db.query(User).filter(User.username == 'admin').first()
        
        if not admin:
            print("ERROR: Admin account not found!")
            print("Please create an admin account first.")
            return False
        
        # Update the email
        old_email = admin.email
        admin.email = new_email
        db.commit()
        
        print(f"SUCCESS: Admin email has been updated!")
        print(f"Username: {admin.username}")
        print(f"Old email: {old_email}")
        print(f"New email: {admin.email}")
        print(f"Role: {admin.role}")
        
        return True
        
    except Exception as e:
        print(f"ERROR: Failed to update email: {e}")
        db.rollback()
        return False
        
    finally:
        db.close()

if __name__ == "__main__":
    import sys
    
    # Allow custom email from command line
    email = sys.argv[1] if len(sys.argv) > 1 else "admin@avionav.com"
    
    print("=" * 60)
    print("Administrator Email Fix")
    print("=" * 60)
    print()
    
    fix_admin_email(email)
