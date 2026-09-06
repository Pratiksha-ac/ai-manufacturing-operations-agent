import pandas as pd
import psycopg2


DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "manufacturing_db",
    "user": "postgres",
    "password": "Postgres@123"
}


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def load_telemetry():
    connection = get_connection()

    query = """
        SELECT
            machine_id,
            timestamp,
            temperature,
            vibration,
            pressure,
            rpm,
            energy_consumption,
            status
        FROM telemetry
        ORDER BY timestamp;
    """

    dataframe = pd.read_sql_query(query, connection)

    connection.close()

    return dataframe


def create_features(dataframe):
    features = dataframe[
        [
            "temperature",
            "vibration",
            "pressure",
            "rpm",
            "energy_consumption"
        ]
    ].copy()

    return features


if __name__ == "__main__":
    dataframe = load_telemetry()

    print("Raw telemetry data:")
    print(dataframe.head())

    features = create_features(dataframe)

    print("\nML features:")
    print(features.head())

    print("\nFeature shape:")
    print(features.shape)