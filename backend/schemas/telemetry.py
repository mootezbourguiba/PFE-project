from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class TelemetryScenario(str, Enum):
    """
    Simulation scenarios supported by the telemetry generator.
    """

    HEALTHY = "healthy"
    BEARING_WEAR = "bearing_wear"


class TelemetrySource(str, Enum):
    """
    Controlled source values for a telemetry record.
    """

    SIMULATED = "simulated"
    UPLOADED = "uploaded"
    MANUAL = "manual"


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


class TelemetryBase(BaseModel):
    """
    Base fields for a telemetry reading.
    """

    timestamp: datetime
    current: float = Field(..., description="Motor current (A)")
    temperature: float = Field(..., description="Motor temperature (°C)")
    source: Optional[TelemetrySource] = Field(
        default=TelemetrySource.MANUAL,
        description="How this reading was produced",
    )


class TelemetryCreate(TelemetryBase):
    """
    Schema for creating a telemetry reading.
    """

    anomaly: Optional[bool] = Field(
        default=None,
        description="Optional ground-truth anomaly label",
    )


class TelemetryResponse(TelemetryBase):
    """
    Schema for returning a stored telemetry reading.
    """

    id: int
    user_id: int
    anomaly: Optional[bool]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TelemetryList(BaseModel):
    """
    Schema for a paginated list of telemetry readings.
    """

    total: int
    items: List[TelemetryResponse]


class TelemetrySimulationRequest(BaseModel):
    """
    Schema for requesting a simulated telemetry flight.
    """

    samples: int = Field(
        default=100,
        ge=1,
        le=10000,
        description="Number of telemetry samples to generate",
    )
    scenario: TelemetryScenario = Field(
        default=TelemetryScenario.HEALTHY,
        description="Simulation scenario: healthy or bearing_wear",
    )
    wear_start: Optional[int] = Field(
        default=None,
        ge=0,
        description="Sample index at which bearing-wear degradation begins",
    )
    seed: Optional[int] = Field(
        default=None,
        description="Optional random seed for reproducible simulation",
    )


class TelemetryLatest(BaseModel):
    """
    Schema for the most recent telemetry reading with prediction.
    """

    reading: Optional[TelemetryResponse] = Field(
        default=None,
        description="The most recent stored telemetry reading",
    )
    prediction: Optional[str] = Field(
        default=None,
        description="HEALTHY or ANOMALY",
    )
    score: Optional[float] = Field(
        default=None,
        description="Isolation Forest decision score",
    )
    recommendation: str = Field(
        ...,
        description="Deterministic maintenance recommendation",
    )


class TelemetryStats(BaseModel):
    """
    Schema for telemetry aggregate counts.
    """

    total_readings: int
    healthy_readings: int
    anomalous_readings: int
    last_reading_at: Optional[datetime]
    latest_prediction: Optional[str]
    latest_score: Optional[float]
