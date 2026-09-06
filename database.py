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


def insert_telemetry(telemetry):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            INSERT INTO telemetry (
                machine_id,
                timestamp,
                temperature,
                vibration,
                pressure,
                rpm,
                energy_consumption,
                status
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            telemetry["machine_id"],
            telemetry["timestamp"],
            telemetry["temperature"],
            telemetry["vibration"],
            telemetry["pressure"],
            telemetry["rpm"],
            telemetry["energy_consumption"],
            telemetry["status"]
        )

        cursor.execute(query, values)

        connection.commit()

        print("Telemetry saved to PostgreSQL!")

    except Exception as e:
        if connection:
            connection.rollback()

        print("Failed to save telemetry:")
        print(e)

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()