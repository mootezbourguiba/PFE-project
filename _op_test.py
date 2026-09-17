import requests

BASE = 'http://localhost:8000/api/v1'
op = {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJvcGVyYXRvcl90ZXN0IiwidXNlcl9pZCI6MTAsInJvbGUiOiJkcm9uZV9vcGVyYXRvciIsImV4cCI6MTc4OTc0Njg3N30.2jZ7-4J3UcUnVFRggN_q2r7AIINGt4RXBnyoYd1lbRA'}
me = {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtYWludDEiLCJ1c2VyX2lkIjozLCJyb2xlIjoibWFpbnRlbmFuY2VfZW5naW5lZXIiLCJleHAiOjE3ODk3NDY4Nzd9.CJ7aT2wJCZc9hd_oE-nAQygFJWIN9OMVnKkCiVlQ_60'}

def check(name, cond, extra=''):
    print(f"{'PASS' if cond else 'FAIL'}  {name}  {extra}")

# CASE 1 — operator /latest
r = requests.get(f'{BASE}/telemetry/latest', headers=op)
d = r.json() if r.status_code == 200 else {}
rd = d.get('reading') or {}
check('C1 GET /telemetry/latest -> 200', r.status_code == 200)
print(f'     reading: ts={rd.get("timestamp")} current={rd.get("current")} temp={rd.get("temperature")} owner_id={rd.get("user_id")}')
print(f'     prediction={d.get("prediction")} score={d.get("score")} recommendation={d.get("recommendation")}')

# CASE 2 — operator list limit=50 skip=0
r = requests.get(f'{BASE}/telemetry/', params={'limit': 50, 'skip': 0}, headers=op)
items = r.json().get('items', []) if r.status_code == 200 else []
owners = sorted({i.get('user_id') for i in items})
check('C2 GET /telemetry/?limit=50 -> 200', r.status_code == 200)
check('C2 returns <=50 items', len(items) <= 50, f'items={len(items)} total={r.json().get("total")}')
print(f'     distinct owner ids in response: {owners} (10 = operator_test)')
ts = [i['timestamp'] for i in items]
check('C2 ordered newest-first', ts == sorted(ts, reverse=True))

# CASE 3 — operator limit=100 -> 403
r = requests.get(f'{BASE}/telemetry/', params={'limit': 100, 'skip': 0}, headers=op)
check('C3 GET /telemetry/?limit=100 -> 403', r.status_code == 403, f'got {r.status_code}')

# CASE 4 — operator skip=1 -> 403
r = requests.get(f'{BASE}/telemetry/', params={'limit': 50, 'skip': 1}, headers=op)
check('C4 GET /telemetry/?skip=1 -> 403', r.status_code == 403, f'got {r.status_code}')

# CASE 5 — operator ingest -> 403
r = requests.post(f'{BASE}/telemetry/', json=[{'timestamp': '2026-09-17T00:00:00', 'current': 15.0, 'temperature': 45.0}], headers=op)
check('C5 POST /telemetry/ -> 403', r.status_code == 403, f'got {r.status_code}')

# CASE 6 — operator simulate -> 403
r = requests.post(f'{BASE}/telemetry/simulate', json={'samples': 5, 'scenario': 'healthy', 'seed': 1}, headers=op)
check('C6 POST /telemetry/simulate -> 403', r.status_code == 403, f'got {r.status_code}')

# CASE 7 — operator upload -> 403
r = requests.post(f'{BASE}/telemetry/upload', files={'file': ('t.csv', 'timestamp,current,temperature\n2026-09-17T00:00:00,15,45\n', 'text/csv')}, headers=op)
check('C7 POST /telemetry/upload -> 403', r.status_code == 403, f'got {r.status_code}')

# CASE 8 — operator stats -> 403
r = requests.get(f'{BASE}/telemetry/stats', headers=op)
check('C8 GET /telemetry/stats -> 403', r.status_code == 403, f'got {r.status_code}')

# CASE 9 — operator users -> 403
r1 = requests.get(f'{BASE}/users/', headers=op)
r2 = requests.post(f'{BASE}/users/', json={'username': 'x', 'email': 'x@x.com', 'password': 'X1234567!', 'role': 'drone_operator'}, headers=op)
check('C9 GET /users/ -> 403', r1.status_code == 403, f'got {r1.status_code}')
check('C9 POST /users/ -> 403', r2.status_code == 403, f'got {r2.status_code}')

# CASE 10 — Maintenance Engineer regression (own-user scoping preserved)
r = requests.get(f'{BASE}/telemetry/latest', headers=me)
d = r.json() if r.status_code == 200 else {}
rd = d.get('reading') or {}
check('C10 ME GET /telemetry/latest -> 200', r.status_code == 200)
check('C10 ME latest is own-user (user_id=3)', rd.get('user_id') == 3, f'owner={rd.get("user_id")}')
r = requests.get(f'{BASE}/telemetry/', params={'limit': 5}, headers=me)
items = r.json().get('items', []) if r.status_code == 200 else []
owners = sorted({i.get('user_id') for i in items})
check('C10 ME list still own-user scoped', owners == [3], f'owners={owners}')
