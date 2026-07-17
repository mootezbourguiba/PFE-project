from pydantic import BaseModel, Field


class TelemetryInput(BaseModel):
    """
    Input telemetry received from the UAV propulsion system.
    """

    current: float = Field(..., gt=0, description="Motor current (A)")
    temperature: float = Field(..., gt=0, description="Motor temperature (°C)")


class TelemetryPrediction(BaseModel):
    """
    Prediction returned by the anomaly detection model.
    """

    prediction: str
    score: float