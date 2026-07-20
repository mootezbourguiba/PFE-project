from backend.database import SessionLocal
from backend.models.user import User
from backend.core.security import verify_password

db = SessionLocal()

user = db.query(User).filter(User.username == "admin").first()

print("=" * 60)

if user is None:
    print("Admin NOT FOUND")
    exit()

print("Username :", user.username)
print("Email    :", user.email)
print("Role     :", user.role)
print("Disabled :", user.disabled)
print()
print("Hash:")
print(user.hashed_password)
print()

print("Password verification")
print("----------------------")
print("Admin123! :", verify_password("Admin123!", user.hashed_password))
print("admin     :", verify_password("admin", user.hashed_password))
print("password  :", verify_password("password", user.hashed_password))