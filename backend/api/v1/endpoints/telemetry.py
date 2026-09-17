from typing import List
from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.dependencies import get_current_maintenance_engineer, get_current_user
from backend.models.user import User
from backend.schemas.telemetry import (
    TelemetryCreate,
    TelemetryInput,
    TelemetryLatest,
    TelemetryList,
    TelemetryPrediction,
    TelemetrySimulationRequest,
    TelemetryStats,
)
from backend.services.telemetry_service import (
    get_latest_telemetry,
    get_telemetry_stats,
    get_user_telemetry,
    ingest_csv,
    ingest_json,
    simulate_telemetry,
)
from backend.ml.anomaly_detector import predict_anomaly

router = APIRouter()


@router.get(
    "/",
    response_model=TelemetryList,
    summary="List telemetry for the authenticated user",
)
def get_telemetry(
    skip: int = Query(0, ge=0),
    limit: int = Query(1000, ge=1, le=10000),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Retrieve telemetry readings belonging to the authenticated user.

    Maintenance Engineers can request full historical telemetry.
    Drone Operators may only view the most recent 50 readings.
    Administrators do not have access to detailed telemetry history.
    """
    if not (current_user.is_maintenance_engineer() or current_user.is_drone_operator()):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized. Maintenance Engineer or Drone Operator access required.",
        )

    if current_user.is_drone_operator() and (limit > 50 or skip != 0):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Drone Operator can only view the most recent 50 telemetry readings.",
        )

    items, total = get_user_telemetry(db, current_user, skip=skip, limit=limit)
    return TelemetryList(total=total, items=items)


@router.get(
    "/latest",
    response_model=TelemetryLatest,
    summary="Get the latest telemetry reading with prediction",
)
def get_latest(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Retrieve the most recent telemetry reading for the authenticated user
    along with the AI prediction and maintenance recommendation.

    Available to Maintenance Engineers and Drone Operators for basic status.
    """
    if not (current_user.is_maintenance_engineer() or current_user.is_drone_operator()):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized. Maintenance Engineer or Drone Operator access required.",
        )

    return TelemetryLatest(
        **get_latest_telemetry(db, current_user)
    )


@router.get(
    "/stats",
    response_model=TelemetryStats,
    summary="Get telemetry statistics for the authenticated user",
)
def get_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Retrieve aggregate telemetry statistics for the authenticated user.

    Available to Administrators for system activity monitoring and to
    Maintenance Engineers.
    """
    if not (current_user.is_administrator() or current_user.is_maintenance_engineer()):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized. Administrator or Maintenance Engineer access required.",
        )

    return TelemetryStats(
        **get_telemetry_stats(db, current_user)
    )


@router.post(
    "/",
    response_model=TelemetryList,
    status_code=status.HTTP_201_CREATED,
    summary="Ingest a JSON list of telemetry readings",
)
def create_telemetry(
    data: List[TelemetryCreate],
    current_user: User = Depends(get_current_maintenance_engineer),
    db: Session = Depends(get_db),
):
    """
    Persist a JSON list of telemetry readings for the authenticated user.
    """
    if not data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No telemetry readings provided.",
        )

    readings = ingest_json(db, current_user, data)
    return TelemetryList(total=len(readings), items=readings)


@router.post(
    "/simulate",
    response_model=TelemetryList,
    status_code=status.HTTP_201_CREATED,
    summary="Generate and store simulated telemetry",
)
def generate_simulated_telemetry(
    request: TelemetrySimulationRequest,
    current_user: User = Depends(get_current_maintenance_engineer),
    db: Session = Depends(get_db),
):
    """
    Generate a smooth, deterministic telemetry time series and store it.

    The generated data is owned by the authenticated user and can be
    retrieved via GET /api/v1/telemetry/.
    """
    readings = simulate_telemetry(db, current_user, request)
    return TelemetryList(total=len(readings), items=readings)


@router.post(
    "/upload",
    response_model=TelemetryList,
    status_code=status.HTTP_201_CREATED,
    summary="Upload and store a telemetry CSV file",
)
def upload_telemetry_csv(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_maintenance_engineer),
    db: Session = Depends(get_db),
):
    """
    Validate and persist a CSV file containing telemetry readings.

    Required columns:
    - timestamp
    - current (or motor_current)
    - temperature (or motor_temperature)

    Optional columns:
    - anomaly
    """
    readings = ingest_csv(db, current_user, file)
    return TelemetryList(total=len(readings), items=readings)


@router.post(
    "/predict",
    response_model=TelemetryPrediction,
    summary="Predict UAV motor anomaly",
)
def predict(
    data: TelemetryInput,
    current_user: User = Depends(get_current_maintenance_engineer),
):
    """
    Predict whether telemetry indicates healthy operation or bearing wear.

    Requires a valid JWT token.
    """
    result = predict_anomaly(
        current=data.current,
        temperature=data.temperature,
    )

    return TelemetryPrediction(
        prediction=result["prediction"],
        score=result["score"],
    )
