import sqlite3
import sys
sys.path.insert(0, '.')
from backend.core.security import verify_password

conn = sqlite3.connect('avionics.db')
c = conn.cursor()
c.execute("SELECT id, username, hashed_password FROM user WHERE username IN ('op1','test_operator','test_create')")
rows = c.fetchall()
conn.close()

candidates = {
    'op1': ['Op1Test123!', 'Op1123!', 'Operator123!', 'Test123!', 'op1test'],
    'test_operator': ['Test123!', 'Operator123!', 'TestOp123!', 'TestOperator123!'],
    'test_create': ['Test123!', 'Create123!', 'TestCreate123!'],
}

for uid, uname, hashed in rows:
    matched = [p for p in candidates.get(uname, []) if verify_password(p, hashed)]
    print(uname, '->', matched if matched else 'no match')
