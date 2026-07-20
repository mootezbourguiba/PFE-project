"""
Authentication Diagnostic Script

This script investigates why authentication fails by:
1. Checking which database file FastAPI uses
2. Checking which database file the password reset script modified
3. Verifying they are the same file
4. Testing if the password hash matches
"""

import os
import sqlite3
from backend.database import DATABASE_URL, engine
from backend.core.security import verify_password

def diagnose():
    print("=" * 70)
    print("Authentication Diagnostic")
    print("=" * 70)
    print()
    
    # 1. Check DATABASE_URL from application
    print("1. FastAPI Database Configuration:")
    print(f"   DATABASE_URL: {DATABASE_URL}")
    print()
    
    # 2. Extract absolute path from DATABASE_URL
    if DATABASE_URL.startswith("sqlite:///"):
        db_path = DATABASE_URL.replace("sqlite:///", "")
        # Convert to absolute path
        if not os.path.isabs(db_path):
            db_path = os.path.abspath(db_path)
        print(f"   Absolute Path: {db_path}")
        print(f"   File Exists: {os.path.exists(db_path)}")
        print()
    else:
        print("   ERROR: Not using SQLite database!")
        return
    
    # 3. Check if database file exists
    if not os.path.exists(db_path):
        print(f"   ERROR: Database file does not exist: {db_path}")
        return
    
    # 4. Query the admin user directly from the database
    print("2. Querying Admin User from Database:")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT id, username, email, role, hashed_password, disabled FROM user WHERE username = 'admin'")
        admin = cursor.fetchone()
        
        if admin:
            print(f"   Admin User Found:")
            print(f"     ID: {admin[0]}")
            print(f"     Username: {admin[1]}")
            print(f"     Email: {admin[2]}")
            print(f"     Role: {admin[3]}")
            print(f"     Disabled: {admin[5]}")
            print(f"     Hashed Password: {admin[4][:50]}...")
            print()
            
            # 5. Test password verification
            print("3. Testing Password Verification:")
            test_password = "Admin123!"
            hashed_password = admin[4]
            
            try:
                result = verify_password(test_password, hashed_password)
                print(f"   Password '{test_password}' matches hash: {result}")
                print()
                
                if not result:
                    print("   ERROR: Password does NOT match!")
                    print("   The password hash in the database does not match 'Admin123!'")
                    print("   This explains why login returns HTTP 401.")
                    print()
                    return False
                else:
                    print("   SUCCESS: Password matches!")
                    print("   Login should work with username='admin' and password='Admin123!'")
                    print()
                    return True
                    
            except Exception as e:
                print(f"   ERROR during password verification: {e}")
                print()
                return False
        else:
            print("   ERROR: No admin user found in database!")
            print()
            return False
            
    except Exception as e:
        print(f"   ERROR querying database: {e}")
        print()
        return False
    finally:
        conn.close()
    
    print("=" * 70)

if __name__ == "__main__":
    diagnose()
