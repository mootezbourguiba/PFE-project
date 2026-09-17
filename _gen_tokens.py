import sys
sys.path.insert(0, '.')
from backend.database import SessionLocal
from backend.models.user import User
from backend.services.auth_service import AuthService

db = SessionLocal()
users = db.query(User).order_by(User.id).all()
with open('_tokens.txt', 'w') as f:
    for u in users:
        t = AuthService.create_token_for_user(u)
        tok = t.access_token if hasattr(t, 'access_token') else t['access_token']
        f.write(f'{u.username}|{u.role}|{tok}\n')
        print(u.username, u.role)
db.close()
