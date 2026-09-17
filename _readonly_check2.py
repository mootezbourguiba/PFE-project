import sqlite3
conn = sqlite3.connect('avionics.db')
c = conn.cursor()
c.execute("SELECT MIN(id), MAX(id), MIN(timestamp), MAX(timestamp), MIN(created_at), MAX(created_at), COUNT(*) FROM telemetryreading WHERE id >= 316 GROUP BY (id-316)/10")
for r in c.fetchall():
    print(r)
print('--- distinct created_at for id>=316 ---')
c.execute("SELECT id, created_at FROM telemetryreading WHERE id IN (316,326,336,346)")
for r in c.fetchall():
    print(r)
conn.close()
