from backend.database import SessionLocal
from backend.models.user import User

db = SessionLocal()
admin = db.query(User).filter(User.username == 'admin').first()

if admin:
    print(f'Admin exists: True')
    print(f'Username: {admin.username}')
    print(f'Role: {admin.role}')
    print(f'Email: {admin.email}')
else:
    print('Admin exists: False')

db.close()
