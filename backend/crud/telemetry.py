from typing import List, Optional
from sqlalchemy.orm import Session
from backend.models.telemetry import TelemetryReading


class CRUDTelemetry:
    """
    CRUD operations for TelemetryReading.
    """

    @staticmethod
    def create_many(
        db: Session,
        readings: List[TelemetryReading],
    ) -> List[TelemetryReading]:
        """
        Persist a list of telemetry readings.
        """
        db.add_all(readings)
        db.commit()
        for reading in readings:
            db.refresh(reading)
        return readings

    @staticmethod
    def get_by_user(
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 1000,
    ) -> List[TelemetryReading]:
        """
        Retrieve telemetry readings for a single user, sorted newest first.
        """
        return (
            db.query(TelemetryReading)
            .filter(TelemetryReading.user_id == user_id)
            .order_by(TelemetryReading.timestamp.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def count_by_user(
        db: Session,
        user_id: int,
    ) -> int:
        """
        Count telemetry readings for a single user.
        """
        return (
            db.query(TelemetryReading)
            .filter(TelemetryReading.user_id == user_id)
            .count()
        )

    @staticmethod
    def get_by_id(
        db: Session,
        reading_id: int,
        user_id: int,
    ) -> Optional[TelemetryReading]:
        """
        Retrieve a single telemetry reading, ensuring it belongs to the user.
        """
        return (
            db.query(TelemetryReading)
            .filter(
                TelemetryReading.id == reading_id,
                TelemetryReading.user_id == user_id,
            )
            .first()
        )


crud_telemetry = CRUDTelemetry()
