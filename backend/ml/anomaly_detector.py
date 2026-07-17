from pathlib import Path

import joblib
import pandas as pd

# Path to the trained model
MODEL_PATH = (
    Path(__file__).resolve().parent
    / "saved_models"
    / "isolation_forest.pkl"
)

# Load the model once when the module is imported
model = joblib.load(MODEL_PATH)


def predict_anomaly(current: float, temperature: float) -> dict:
    """
    Predict whether telemetry corresponds to healthy
    operation or a bearing wear anomaly.
    """

    sample = pd.DataFrame(
        {
            "current": [current],
            "temperature": [temperature],
        }
    )

    prediction = model.predict(sample)[0]
    score = model.decision_function(sample)[0]

    return {
        "prediction": "HEALTHY" if prediction == 1 else "ANOMALY",
        "score": round(float(score), 4),
    }


if __name__ == "__main__":
    print("Loading Isolation Forest model...")

    print("\nHealthy telemetry test:")
    print(predict_anomaly(15.4, 44.2))

    print("\nBearing wear telemetry test:")
    print(predict_anomaly(29.5, 88.4))