from sklearn.ensemble import IsolationForest

from features import load_telemetry, create_features


def detect_anomalies():

    dataframe = load_telemetry()

    features = create_features(dataframe)

    model = IsolationForest(
        contamination=0.05,
        random_state=42
    )

    model.fit(features)

    predictions = model.predict(features)

    dataframe["anomaly"] = predictions

    return dataframe