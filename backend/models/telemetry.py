"""
Telemetry model.

Stores time-series telemetry readings for UAV propulsion systems.
"""

import enum
from sqlalchemy import Column, Float, Integer, ForeignKey, DateTime, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from backend.models.base import BaseModel


class TelemetrySource(str, enum.Enum):
    """
    Controlled source values for a telemetry record.
    """

    SIMULATED = "simulated"
    UPLOADED = "uploaded"
    MANUAL = "manual"


class TelemetryReading(BaseModel):
    """
    Telemetry reading from the UAV propulsion system.

    Each row represents one timestamped observation of motor current and
    motor temperature.  The record is owned by the authenticated user who
    created or uploaded it.
    """

    user_id = Column(
        Integer,
        ForeignKey("user.id"),
        nullable=False,
        index=True,
    )

    timestamp = Column(
        DateTime,
        nullable=False,
        index=True,
    )

    current = Column(
        Float,
        nullable=False,
    )

    temperature = Column(
        Float,
        nullable=False,
    )

    anomaly = Column(
        Boolean,
        nullable=True,
        default=None,
    )

    source = Column(
        SQLEnum(
            TelemetrySource,
            name="telemetrysource",
            create_constraint=True,
        ),
        nullable=False,
        default=TelemetrySource.MANUAL,
    )

    user = relationship("User", backref="telemetry_readings")
