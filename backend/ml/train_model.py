import pandas as pd
import joblib
from sklearn.ensemble import IsolationForest
from pathlib import Path


def train_isolation_forest():
    """
    Train Isolation Forest using healthy telemetry data only.
    """

    print("Loading healthy telemetry dataset...")

    dataset_path = Path("datasets/healthy_flight_data.csv")

    df = pd.read_csv(dataset_path)

    print(f"Dataset loaded successfully.")
    print(f"Number of samples: {len(df)}")

    # Keep only the features used by the model
    X = df[["current", "temperature"]]

    print("\nTraining Isolation Forest model...")

    model = IsolationForest(
        contamination=0.01,
        random_state=42
    )

    model.fit(X)

    print("Training completed successfully.")

    model_path = Path(
        "backend/ml/saved_models/isolation_forest.pkl"
    )

    joblib.dump(model, model_path)

    print("\nModel saved successfully:")
    print(model_path)


if __name__ == "__main__":
    train_isolation_forest()