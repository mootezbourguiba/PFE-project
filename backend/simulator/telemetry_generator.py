"""
UAV propulsion telemetry simulator.

Generates smooth, temporally continuous time series of motor current and
motor temperature.  Healthy flights oscillate around a stable operating
point.  Bearing-wear flights remain healthy for a configurable period and
then progressively increase both current and temperature.
"""

from datetime import datetime, timedelta
from typing import Optional
import numpy as np


# Healthy operating point
HEALTHY_CURRENT_MEAN = 15.0
HEALTHY_CURRENT_STD = 0.6
HEALTHY_TEMPERATURE_MEAN = 42.0
HEALTHY_TEMPERATURE_STD = 0.8

# Thermal coupling: temperature rise due to Joule heating is proportional
# to the square of the current above the baseline.
THERMAL_COEFFICIENT = 0.045

# Minimum physically reasonable limits.
MIN_CURRENT = 0.0
MIN_TEMPERATURE = -273.15


def _clamp(value, min_value, max_value):
    return np.clip(value, min_value, max_value)


def generate_telemetry_data(
    samples: int = 100,
    anomaly: bool = False,
    wear_start: Optional[int] = None,
    seed: Optional[int] = None,
    start_time: Optional[datetime] = None,
):
    """
    Generate synthetic UAV propulsion telemetry.

    Parameters
    ----------
    samples : int
        Number of telemetry samples to generate.
    anomaly : bool
        False -> healthy flight data
        True  -> progressive bearing-wear data
    wear_start : int, optional
        Sample index at which bearing-wear degradation begins.  If not
        provided, defaults to 30% of the sample count for anomalous data.
    seed : int, optional
        Random seed for reproducible output.
    start_time : datetime, optional
        Timestamp of the first sample.  Defaults to the current UTC time.

    Returns
    -------
    list
        List of telemetry dictionaries with keys:
        timestamp (datetime), current (float), temperature (float),
        anomaly (bool).
    """
    if samples <= 0:
        raise ValueError("samples must be positive")

    rng = np.random.default_rng(seed)

    if start_time is None:
        start_time = datetime.utcnow()

    if anomaly and wear_start is None:
        wear_start = int(samples * 0.3)
    if not anomaly:
        wear_start = samples + 1

    # Healthy current as a smooth bounded random walk.
    current = np.zeros(samples)
    current[0] = HEALTHY_CURRENT_MEAN + rng.normal(0.0, 0.2)
    for t in range(1, samples):
        # AR(1) process: current reverts to the mean with additive noise.
        shock = rng.normal(0.0, HEALTHY_CURRENT_STD * 0.3)
        current[t] = 0.92 * (current[t - 1] - HEALTHY_CURRENT_MEAN) + HEALTHY_CURRENT_MEAN + shock

    # Healthy temperature driven by current through thermal coupling.
    temperature = np.zeros(samples)
    temperature[0] = HEALTHY_TEMPERATURE_MEAN + rng.normal(0.0, 0.2)
    for t in range(1, samples):
        joule_heat = THERMAL_COEFFICIENT * (current[t] ** 2)
        target_temp = HEALTHY_TEMPERATURE_MEAN + joule_heat
        shock = rng.normal(0.0, HEALTHY_TEMPERATURE_STD * 0.3)
        # Exponential smoothing with the previous sample to keep continuity.
        temperature[t] = 0.85 * temperature[t - 1] + 0.15 * target_temp + shock

    # Labels: False until the wear-start point, then True for the anomaly.
    anomaly_flags = [False] * samples

    # Apply progressive bearing-wear degradation after wear_start.
    if anomaly:
        for t in range(wear_start, samples):
            # Progressive bearing-wear: current and temperature drift upward
            # in a roughly linear fashion with a small noise term.
            elapsed = t - wear_start
            current_drift = 0.08 * elapsed
            temperature_drift = 0.25 * elapsed

            current[t] += current_drift + 0.15 * rng.normal()
            temperature[t] += temperature_drift + 0.25 * rng.normal()

            # After wear starts, the observations are anomalous.
            anomaly_flags[t] = True

    # Clamp to physically reasonable bounds.
    current = np.round(_clamp(current, MIN_CURRENT, 100.0), 2)
    temperature = np.round(_clamp(temperature, MIN_TEMPERATURE, 200.0), 2)

    data = []
    timestamp = start_time
    for t in range(samples):
        data.append(
            {
                "timestamp": timestamp,
                "current": float(current[t]),
                "temperature": float(temperature[t]),
                "anomaly": bool(anomaly_flags[t]),
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
        f"{'Anomaly':<10}"
    )
    print("-" * 70)

    for row in dataset:
        print(
            f"{row['timestamp']:%Y-%m-%d %H:%M:%S}"
            f"{row['current']:<15}"
            f"{row['temperature']:<20}"
            f"{'True' if row['anomaly'] else 'False'}"
        )


if __name__ == "__main__":
    print("\nHEALTHY FLIGHT DATA\n")
    healthy_data = generate_telemetry_data(samples=30, anomaly=False, seed=42)
    print_dataset(healthy_data)

    print("\n" + "=" * 70 + "\n")
    print("BEARING WEAR ANOMALY DATA\n")
    anomaly_data = generate_telemetry_data(
        samples=30, anomaly=True, wear_start=10, seed=42
    )
    print_dataset(anomaly_data)
