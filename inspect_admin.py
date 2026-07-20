"""
Inspect Administrator Account Script

This script displays the current administrator account details from the database.
"""

from backend.database import SessionLocal
from backend.models.user import User

def inspect_admin():
    """
    Display administrator account details.
    """
    db = SessionLocal()
    
    try:
        # Find the admin user
        admin = db.query(User).filter(User.username == 'admin').first()
        
        if not admin:
            print("No administrator account found in the database.")
            print("You need to create an admin account first.")
            return
        
        print("=" * 60)
        print("Administrator Account Details")
        print("=" * 60)
        print()
        print(f"ID:              {admin.id}")
        print(f"Username:        {admin.username}")
        print(f"Email:           {admin.email}")
        print(f"Role:            {admin.role}")
        print(f"Disabled:        {admin.disabled}")
        print(f"Disabled Reason: {admin.disabled_reason}")
        print(f"Created At:      {admin.created_at}")
        print(f"Updated At:      {admin.updated_at}")
        print()
        print("Password Status:")
        print(f"  Hashed Password: {admin.hashed_password[:50]}... (truncated for security)")
        print(f"  Note: Password is hashed and cannot be recovered.")
        print()
        print("=" * 60)
        
    except Exception as e:
        print(f"ERROR: Failed to inspect admin account: {e}")
        
    finally:
        db.close()

if __name__ == "__main__":
    inspect_admin()
