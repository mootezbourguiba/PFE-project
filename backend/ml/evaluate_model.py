import pandas as pd
import joblib

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)


def evaluate_model():

    print("Loading trained model...")
    model = joblib.load(
        "backend/ml/saved_models/isolation_forest.pkl"
    )

    print("Loading evaluation datasets...")

    healthy_df = pd.read_csv(
        "datasets/healthy_flight_data.csv"
    )

    anomaly_df = pd.read_csv(
        "datasets/bearing_wear_data.csv"
    )

    # Ground truth labels
    healthy_df["true_label"] = 1
    anomaly_df["true_label"] = -1

    evaluation_df = pd.concat(
        [healthy_df, anomaly_df],
        ignore_index=True
    )

    X = evaluation_df[
        ["current", "temperature"]
    ]

    y_true = evaluation_df["true_label"]

    print("Running predictions...")

    y_pred = model.predict(X)

    accuracy = accuracy_score(
        y_true,
        y_pred
    )

    precision = precision_score(
        y_true,
        y_pred,
        pos_label=-1
    )

    recall = recall_score(
        y_true,
        y_pred,
        pos_label=-1
    )

    f1 = f1_score(
        y_true,
        y_pred,
        pos_label=-1
    )

    cm = confusion_matrix(
        y_true,
        y_pred,
        labels=[1, -1]
    )

    print("\n========== RESULTS ==========")

    print(f"Accuracy  : {accuracy:.4f}")
    print(f"Precision : {precision:.4f}")
    print(f"Recall    : {recall:.4f}")
    print(f"F1 Score  : {f1:.4f}")

    print("\nConfusion Matrix")
    print(cm)

    print("\nLegend:")
    print("Rows    -> Actual")
    print("Columns -> Predicted")
    print("[[Healthy, Anomaly],")
    print(" [Healthy, Anomaly]]")


if __name__ == "__main__":
    evaluate_model()