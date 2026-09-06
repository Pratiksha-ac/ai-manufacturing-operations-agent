import pandas as pd
from sklearn.ensemble import IsolationForest

from features import load_telemetry, create_features


def detect_anomalies():

    # Load raw telemetry
    dataframe = load_telemetry()

    # Create ML features
    features = create_features(dataframe)

    # Create model
    model = IsolationForest(
        contamination=0.05,
        random_state=42
    )

    # Train model
    model.fit(features)

    # Predict anomalies
    predictions = model.predict(features)

    # Add predictions to original data
    dataframe["anomaly"] = predictions

    return dataframe


if __name__ == "__main__":

    results = detect_anomalies()

    print("\nAnomaly Detection Results")
    print("=" * 80)

    print(
        results[
            [
                "machine_id",
                "temperature",
                "vibration",
                "pressure",
                "energy_consumption",
                "anomaly"
            ]
        ].tail(20)
    )