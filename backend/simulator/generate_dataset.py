import csv
from backend.simulator.telemetry_generator import generate_telemetry_data


HEALTHY_SAMPLES = 1000
ANOMALY_SAMPLES = 300


healthy_data = generate_telemetry_data(
    samples=HEALTHY_SAMPLES,
    anomaly=False
)

anomaly_data = generate_telemetry_data(
    samples=ANOMALY_SAMPLES,
    anomaly=True
)


with open(
    "datasets/healthy_flight_data.csv",
    mode="w",
    newline=""
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=[
            "timestamp",
            "current",
            "temperature",
            "anomaly"
        ]
    )

    writer.writeheader()
    writer.writerows(healthy_data)


with open(
    "datasets/bearing_wear_data.csv",
    mode="w",
    newline=""
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=[
            "timestamp",
            "current",
            "temperature",
            "anomaly"
        ]
    )

    writer.writeheader()
    writer.writerows(anomaly_data)


print()
print("Datasets successfully generated.")
print()

print(
    f"Healthy samples: {HEALTHY_SAMPLES}"
)

print(
    f"Anomaly samples: {ANOMALY_SAMPLES}"
)

print()
print("Files created:")
print("datasets/healthy_flight_data.csv")
print("datasets/bearing_wear_data.csv")