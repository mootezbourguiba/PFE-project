import io
import math
from datetime import datetime
from typing import List, Optional
import pandas as pd
from fastapi import HTTPException, status, UploadFile
from sqlalchemy.orm import Session

from backend.crud.telemetry import crud_telemetry
from backend.models.telemetry import TelemetryReading, TelemetrySource
from backend.models.user import User
from backend.schemas.telemetry import (
    TelemetryCreate,
    TelemetryScenario,
    TelemetrySimulationRequest,
)
from backend.simulator.telemetry_generator import generate_telemetry_data
from backend.ml.anomaly_detector import predict_anomaly


# Conservative validation limits for obviously invalid telemetry values.
# Current cannot be negative for a DC motor.
# Temperature is constrained to be above absolute zero.
MIN_CURRENT = 0.0
MIN_TEMPERATURE = -273.15


def _validate_value(value, name, min_value):
    """
    Validate a single numeric telemetry value.
    """
    if value is None or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a number")
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    if value <= min_value:
        raise ValueError(f"{name} is below the minimum acceptable value {min_value}")
    return float(value)


def _readings_to_model(
    user: User,
    rows: List[dict],
    source: TelemetrySource,
) -> List[TelemetryReading]:
    """
    Convert validated dictionaries to TelemetryReading model instances.
    """
    readings = []
    for row in rows:
        readings.append(
            TelemetryReading(
                user_id=user.id,
                timestamp=row["timestamp"],
                current=row["current"],
                temperature=row["temperature"],
                anomaly=row.get("anomaly"),
                source=source,
            )
        )
    return readings


def simulate_telemetry(
    db: Session,
    user: User,
    request: TelemetrySimulationRequest,
) -> List[TelemetryReading]:
    """
    Generate a smooth, deterministic telemetry time series and persist it.
    """
    scenario = request.scenario
    if scenario == TelemetryScenario.HEALTHY:
        anomaly = False
    else:
        anomaly = True

    wear_start = request.wear_start
    if scenario == TelemetryScenario.BEARING_WEAR and wear_start is None:
        # Default: begin degradation after 30% of samples.
        wear_start = int(request.samples * 0.3)

    raw_data = generate_telemetry_data(
        samples=request.samples,
        anomaly=anomaly,
        wear_start=wear_start,
        seed=request.seed,
    )

    # The generator always returns a controlled simulated source.
    source = TelemetrySource.SIMULATED

    readings = _readings_to_model(user, raw_data, source)
    return crud_telemetry.create_many(db, readings)


def ingest_json(
    db: Session,
    user: User,
    items: List[TelemetryCreate],
) -> List[TelemetryReading]:
    """
    Validate and persist a JSON list of telemetry readings.
    """
    rows = []
    for item in items:
        _validate_value(item.current, "current", MIN_CURRENT)
        _validate_value(item.temperature, "temperature", MIN_TEMPERATURE)

        rows.append(
            {
                "timestamp": item.timestamp,
                "current": item.current,
                "temperature": item.temperature,
                "anomaly": item.anomaly,
            }
        )

    readings = _readings_to_model(user, rows, TelemetrySource.MANUAL)
    return crud_telemetry.create_many(db, readings)


def _parse_csv_content(content: bytes) -> pd.DataFrame:
    """
    Read and minimally validate a CSV payload.
    """
    try:
        df = pd.read_csv(io.BytesIO(content))
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unable to read CSV file: {exc}",
        )

    if df.empty:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CSV file is empty",
        )

    # Accept either 'current'/'temperature' or the prefixed variants.
    df.columns = [c.strip().lower() for c in df.columns]

    column_map = {}
    for expected in ("timestamp", "current", "temperature"):
        column_map[expected] = None
        if expected in df.columns:
            column_map[expected] = expected

    if column_map["current"] is None and "motor_current" in df.columns:
        column_map["current"] = "motor_current"
    if column_map["temperature"] is None and "motor_temperature" in df.columns:
        column_map["temperature"] = "motor_temperature"

    missing = [name for name, col in column_map.items() if col is None]
    if missing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"CSV missing required columns: {', '.join(missing)}. "
            "Expected at least: timestamp, current (or motor_current), "
            "temperature (or motor_temperature).",
        )

    return df.rename(
        columns={
            column_map["current"]: "current",
            column_map["temperature"]: "temperature",
        }
    )


def ingest_csv(
    db: Session,
    user: User,
    file: UploadFile,
) -> List[TelemetryReading]:
    """
    Validate and persist a CSV file of telemetry readings.
    """
    content = file.file.read()
    if not content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty",
        )

    df = _parse_csv_content(content)

    # Ensure the timestamp column can be parsed.
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    if df["timestamp"].isna().any():
        bad_rows = df["timestamp"].isna().sum()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Could not parse {bad_rows} timestamp value(s).",
        )

    # Validate numeric columns.
    df["current"] = pd.to_numeric(df["current"], errors="coerce")
    df["temperature"] = pd.to_numeric(df["temperature"], errors="coerce")

    if df["current"].isna().any() or df["temperature"].isna().any():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CSV contains non-numeric current or temperature values.",
        )

    if (df["current"] <= MIN_CURRENT).any():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"CSV contains current values below {MIN_CURRENT} A.",
        )

    if (df["temperature"] <= MIN_TEMPERATURE).any():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"CSV contains temperature values below {MIN_TEMPERATURE} °C.",
        )

    rows = []
    has_anomaly = "anomaly" in df.columns
    for _, row in df.iterrows():
        anomaly = None
        if has_anomaly:
            raw = row["anomaly"]
            if isinstance(raw, bool):
                anomaly = raw
            elif isinstance(raw, (int, float)):
                anomaly = bool(raw)
            elif isinstance(raw, str):
                anomaly = raw.strip().lower() in ("1", "true", "yes")

        rows.append(
            {
                "timestamp": row["timestamp"].to_pydatetime(),
                "current": float(row["current"]),
                "temperature": float(row["temperature"]),
                "anomaly": anomaly,
            }
        )

    readings = _readings_to_model(user, rows, TelemetrySource.UPLOADED)
    return crud_telemetry.create_many(db, readings)


def get_user_telemetry(
    db: Session,
    user: User,
    skip: int = 0,
    limit: int = 1000,
) -> tuple:
    """
    Return the telemetry data and count for the authenticated user.

    Drone Operators consume the shared operational feed: the newest
    system-wide readings rather than user-owned records.
    """
    if user.is_drone_operator():
        items = (
            db.query(TelemetryReading)
            .order_by(TelemetryReading.timestamp.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        total = db.query(TelemetryReading).count()
        return items, total
    items = crud_telemetry.get_by_user(db, user.id, skip=skip, limit=limit)
    total = crud_telemetry.count_by_user(db, user.id)
    return items, total


def _get_recommendation(prediction: Optional[str]) -> str:
    """
    Return a deterministic maintenance recommendation from a prediction.
    """
    if prediction == "HEALTHY":
        return "Normal operation"
    if prediction == "ANOMALY":
        return "Maintenance inspection recommended"
    return "No telemetry available. Generate or upload telemetry."


def get_latest_telemetry(db: Session, user: User):
    """
    Return the most recent telemetry reading for a user and its AI prediction.

    Drone Operators monitor the shared operational feed: the newest
    system-wide reading rather than a user-owned record.
    """
    query = db.query(TelemetryReading)
    if not user.is_drone_operator():
        query = query.filter(TelemetryReading.user_id == user.id)
    reading = query.order_by(TelemetryReading.timestamp.desc()).first()

    if not reading:
        return {
            "reading": None,
            "prediction": None,
            "score": None,
            "recommendation": _get_recommendation(None),
        }

    try:
        result = predict_anomaly(
            current=reading.current,
            temperature=reading.temperature,
        )
        prediction = result["prediction"]
        score = result["score"]
    except Exception:
        prediction = None
        score = None

    return {
        "reading": reading,
        "prediction": prediction,
        "score": score,
        "recommendation": _get_recommendation(prediction),
    }


def get_telemetry_stats(db: Session, user: User):
    """
    Return aggregate telemetry counts for the authenticated user.
    """
    total = crud_telemetry.count_by_user(db, user.id)
    anomalous = (
        db.query(TelemetryReading)
        .filter(
            TelemetryReading.user_id == user.id,
            TelemetryReading.anomaly == True,
        )
        .count()
    )
    healthy = (
        db.query(TelemetryReading)
        .filter(
            TelemetryReading.user_id == user.id,
            TelemetryReading.anomaly == False,
        )
        .count()
    )

    latest = (
        db.query(TelemetryReading)
        .filter(TelemetryReading.user_id == user.id)
        .order_by(TelemetryReading.timestamp.desc())
        .first()
    )

    latest_prediction = None
    latest_score = None
    if latest:
        try:
            result = predict_anomaly(
                current=latest.current,
                temperature=latest.temperature,
            )
            latest_prediction = result["prediction"]
            latest_score = result["score"]
        except Exception:
            pass

    return {
        "total_readings": total,
        "healthy_readings": healthy,
        "anomalous_readings": anomalous,
        "last_reading_at": latest.timestamp if latest else None,
        "latest_prediction": latest_prediction,
        "latest_score": latest_score,
    }
