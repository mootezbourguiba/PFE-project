from datetime import datetime, timedelta
import random


def generate_telemetry_data(
    samples=30,
    anomaly=False
):
    """
    Generate synthetic UAV propulsion telemetry.

    Parameters
    ----------
    samples : int
        Number of telemetry samples to generate.

    anomaly : bool
        False -> healthy flight data
        True  -> bearing wear anomaly data

    Returns
    -------
    list
        List of telemetry dictionaries.
    """

    data = []

    timestamp = datetime.now()

    if anomaly:
        current = 18.0
        temperature = 55.0
    else:
        current = 15.0
        temperature = 40.0

    for _ in range(samples):

        if anomaly:
            # Progressive bearing wear behaviour
            current += random.uniform(0.25, 0.60)
            temperature += random.uniform(0.80, 1.80)

        else:
            # Healthy operating conditions
            current = random.uniform(14.0, 18.0)
            temperature = random.uniform(35.0, 55.0)

        data.append(
            {
                "timestamp": timestamp.strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "current": round(current, 2),
                "temperature": round(temperature, 2),
                "anomaly": anomaly
            }
        )

        timestamp += timedelta(seconds=1)

    return data


def print_dataset(dataset):
    """
    Pretty print telemetry dataset.
    """

    print(
        f"{'Timestamp':<22}"
        f"{'Current(A)':<15}"
        f"{'Temperature(°C)':<20}"
        f"{'Anomaly'}"
    )

    print("-" * 70)

    for row in dataset:
        print(
            f"{row['timestamp']:<22}"
            f"{row['current']:<15}"
            f"{row['temperature']:<20}"
            f"{row['anomaly']}"
        )


if __name__ == "__main__":

    print("\nHEALTHY FLIGHT DATA\n")

    healthy_data = generate_telemetry_data(
        samples=30,
        anomaly=False
    )

    print_dataset(healthy_data)

    print("\n")
    print("=" * 70)
    print("\n")

    print("BEARING WEAR ANOMALY DATA\n")

    anomaly_data = generate_telemetry_data(
        samples=30,
        anomaly=True
    )

    print_dataset(anomaly_data)