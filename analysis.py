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


def analyze_machines():
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT
            machine_id,
            COUNT(*) AS readings,
            AVG(temperature) AS avg_temperature,
            MAX(temperature) AS max_temperature,
            AVG(vibration) AS avg_vibration,
            MAX(vibration) AS max_vibration,
            AVG(pressure) AS avg_pressure,
            MAX(pressure) AS max_pressure,
            AVG(rpm) AS avg_rpm,
            AVG(energy_consumption) AS avg_energy
        FROM telemetry
        GROUP BY machine_id
        ORDER BY machine_id;
    """

    cursor.execute(query)

    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results


if __name__ == "__main__":
    results = analyze_machines()

    print("\nMachine Analysis")
    print("=" * 80)

    for row in results:
        (
            machine_id,
            readings,
            avg_temperature,
            max_temperature,
            avg_vibration,
            max_vibration,
            avg_pressure,
            max_pressure,
            avg_rpm,
            avg_energy
        ) = row

        print(f"\nMachine: {machine_id}")
        print(f"Readings: {readings}")
        print(f"Average Temperature: {avg_temperature:.2f}")
        print(f"Maximum Temperature: {max_temperature:.2f}")
        print(f"Average Vibration: {avg_vibration:.2f}")
        print(f"Maximum Vibration: {max_vibration:.2f}")
        print(f"Average Pressure: {avg_pressure:.2f}")
        print(f"Maximum Pressure: {max_pressure:.2f}")
        print(f"Average RPM: {avg_rpm:.2f}")
        print(f"Average Energy: {avg_energy:.2f}")