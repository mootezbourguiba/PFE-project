import sys
sys.path.insert(0, '.')
from backend.simulator.telemetry_generator import generate_telemetry_data
from backend.ml.anomaly_detector import predict_anomaly

# Find the smallest bearing_wear simulation whose FINAL reading predicts ANOMALY.
# The dashboard shows the model prediction on the latest reading's values.
for samples in (10, 30, 50, 100):
    for seed in (42, 1, 7):
        data = generate_telemetry_data(samples=samples, anomaly=True, seed=seed)
        last = data[-1]
        try:
            r = predict_anomaly(current=last['current'], temperature=last['temperature'])
            print(f"samples={samples} seed={seed}: last=({last['current']}A, {last['temperature']}C) flag={last['anomaly']} -> {r['prediction']} score={r['score']:.4f}")
        except Exception as e:
            print(f"samples={samples} seed={seed}: predict error {e}")
