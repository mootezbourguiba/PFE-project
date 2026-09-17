import sqlite3
conn = sqlite3.connect('avionics.db')
c = conn.cursor()
c.execute("SELECT id, timestamp, current, temperature, anomaly, source, user_id FROM telemetryreading WHERE timestamp >= '2026-09-16' ORDER BY timestamp")
rows = c.fetchall()
print('rows on/after 2026-09-16:', len(rows))
for r in rows:
    print(r)
conn.close()
