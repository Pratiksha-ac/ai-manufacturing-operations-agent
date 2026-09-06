import psycopg2
from langchain_core.tools import tool


DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "manufacturing_db",
    "user": "postgres",
    "password": "Postgres@123"
}


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


@tool
def get_machine_history(machine_id: str, limit: int = 10):
    """
    Retrieve recent telemetry history for a manufacturing machine.

    Use this tool when you need to investigate the recent
    operating behavior of a specific machine.
    """

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT
            timestamp,
            temperature,
            vibration,
            pressure,
            rpm,
            energy_consumption,
            status
        FROM telemetry
        WHERE machine_id = %s
        ORDER BY timestamp DESC
        LIMIT %s;
    """

    cursor.execute(
        query,
        (machine_id, limit)
    )

    results = cursor.fetchall()

    cursor.close()
    connection.close()

    history = []

    for row in results:
        timestamp, temperature, vibration, pressure, rpm, energy, status = row

        history.append({
            "timestamp": str(timestamp),
            "temperature": float(temperature),
            "vibration": float(vibration),
            "pressure": float(pressure),
            "rpm": float(rpm),
            "energy_consumption": float(energy),
            "status": status
        })

    return history


if __name__ == "__main__":

    result = get_machine_history.invoke({
        "machine_id": "CNC-04",
        "limit": 10
    })

    print("\nMachine History")
    print("=" * 100)

    for row in result:
        print(row)

    print("=" * 100)