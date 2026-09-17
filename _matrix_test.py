import requests

BASE = 'http://localhost:8000/api/v1'
accounts = {}
for line in open('_tokens.txt'):
    u, r, t = line.strip().split('|')
    accounts[u] = (r, {'Authorization': f'Bearer {t}'})

def code(r): return r.status_code
def check(name, got, want):
    print(f"{'PASS' if got == want else 'FAIL'}  {name:55s} want={want} got={got}")

print('===== DRONE OPERATORS =====')
for u in ('op1', 'test_operator', 'test_create', 'operator_test'):
    h = accounts[u][1]
    lat = requests.get(f'{BASE}/telemetry/latest', headers=h)
    check(f'{u} GET /latest', code(lat), 200)
    if lat.status_code == 200:
        d = lat.json()
        rd = d.get('reading') or {}
        print(f'      -> pred={d.get("prediction")} rec={d.get("recommendation")} reading={rd.get("current")}A/{rd.get("temperature")}C owner={rd.get("user_id")}')
    check(f'{u} GET /?limit=50', code(requests.get(f'{BASE}/telemetry/', params={'limit': 50, 'skip': 0}, headers=h)), 200)
    check(f'{u} GET /?limit=100', code(requests.get(f'{BASE}/telemetry/', params={'limit': 100}, headers=h)), 403)
    check(f'{u} GET /?skip=1', code(requests.get(f'{BASE}/telemetry/', params={'limit': 50, 'skip': 1}, headers=h)), 403)
    check(f'{u} GET /stats', code(requests.get(f'{BASE}/telemetry/stats', headers=h)), 403)
    check(f'{u} POST /telemetry/', code(requests.post(f'{BASE}/telemetry/', json=[{'timestamp': '2026-01-01T00:00:00', 'current': 1, 'temperature': 1}], headers=h)), 403)
    check(f'{u} POST /simulate', code(requests.post(f'{BASE}/telemetry/simulate', json={'samples': 5, 'scenario': 'healthy'}, headers=h)), 403)
    check(f'{u} POST /upload', code(requests.post(f'{BASE}/telemetry/upload', files={'file': ('t.csv', 'a,b\n1,2\n', 'text/csv')}, headers=h)), 403)
    check(f'{u} POST /predict', code(requests.post(f'{BASE}/telemetry/predict', json={'current': 15.0, 'temperature': 45.0}, headers=h)), 403)
    check(f'{u} GET /users/', code(requests.get(f'{BASE}/users/', headers=h)), 403)

print('===== MAINTENANCE ENGINEERS (read-only checks; writes verified by shared dependency) =====')
for u in ('maint1', 'maint2', 'maint3', 'test_maint', 'test_update', 'test_reset'):
    h = accounts[u][1]
    lat = requests.get(f'{BASE}/telemetry/latest', headers=h)
    check(f'{u} GET /latest', code(lat), 200)
    if lat.status_code == 200:
        rd = (lat.json().get('reading') or {})
        print(f'      -> latest owner={rd.get("user_id")} ts={rd.get("timestamp")}')
    lst = requests.get(f'{BASE}/telemetry/', params={'limit': 5}, headers=h)
    check(f'{u} GET /?limit=5', code(lst), 200)
    if lst.status_code == 200:
        owners = sorted({i.get('user_id') for i in lst.json().get('items', [])})
        print(f'      -> list owners={owners} total={lst.json().get("total")}')
    check(f'{u} GET /stats (ME allowed)', code(requests.get(f'{BASE}/telemetry/stats', headers=h)), 200)
    check(f'{u} POST /predict (ME allowed)', code(requests.post(f'{BASE}/telemetry/predict', json={'current': 15.0, 'temperature': 45.0}, headers=h)), 200)
    check(f'{u} GET /users/ (admin only)', code(requests.get(f'{BASE}/users/', headers=h)), 403)

print('===== ADMINISTRATOR (cross-role spot check) =====')
h = accounts['admin'][1]
check('admin GET /telemetry/latest', code(requests.get(f'{BASE}/telemetry/latest', headers=h)), 403)
check('admin GET /telemetry/', code(requests.get(f'{BASE}/telemetry/', headers=h)), 403)
check('admin GET /stats', code(requests.get(f'{BASE}/telemetry/stats', headers=h)), 200)
check('admin GET /users/', code(requests.get(f'{BASE}/users/', headers=h)), 200)
check('admin POST /simulate', code(requests.post(f'{BASE}/telemetry/simulate', json={'samples': 5, 'scenario': 'healthy'}, headers=h)), 403)
