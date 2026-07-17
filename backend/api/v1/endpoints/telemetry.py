from fastapi import APIRouter
from backend.schemas.telemetry import (
    TelemetryInput,
    TelemetryPrediction,
)
from backend.ml.anomaly_detector import predict_anomaly

router = APIRouter()


@router.post(
    "/predict",
    response_model=TelemetryPrediction,
    summary="Predict UAV motor anomaly",
)
def predict(data: TelemetryInput):
    """
    Predict whether telemetry indicates
    healthy operation or bearing wear.
    """

    result = predict_anomaly(
        current=data.current,
        temperature=data.temperature,
    )

    return TelemetryPrediction(
        prediction=result["prediction"],
        score=result["score"],
    )