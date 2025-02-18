import psycopg2
import os

# Connection parameters
host = "dpg-cuo9l73qf0us738ub4gg-a.frankfurt-postgres.render.com"
port = "5432"
database = "db_261database"
username = "db_261database_user"
password = "vLblDDUVURf4vKa8MExB8d1hiwWAIQg8"

# Function to connect to the database
def getDatabaseConnection():
    try:
        # Attempting to connect to the database
        connection = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=username,
            password=password
        )
        cursor = connection.cursor()
        return connection, cursor
    except Exception as e:
        print(f"Error during database connection: {e}")
        return None, None

    
# Function to close the connection and cursor
def closeDatabaseConnection(connection, cursor):
    try:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
    except Exception as e:
        print(f"Error closing the connection: {e}")

# Function to fetch all tables from the database
def fetchAllTables():
    connection, cursor = getDatabaseConnection()

    if connection is None or cursor is None:
        print("Failed to connect to the database.")
        return []

    try:
        # Example query to fetch all tables in the public schema
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
        
        # Fetch all results from the query
        tables = cursor.fetchall()

        # Output the table names
        print("Tables in the database:")
        for table in tables:
            print(table[0])

        return tables

    except Exception as e:
        print(f"Error fetching tables: {e}")
        return []

    finally:
        # Ensure the connection is closed properly
        closeDatabaseConnection(connection, cursor)

# Insert model traffic flow data
def insertModelTrafficFlowData(InputModelName, InputSimulationTime,
                            InputNorthboundNorth, InputNorthboundEast, InputNorthboundWest, 
                            InputSouthboundSouth, InputSouthboundEast, InputSouthboundWest,
                            InputEastboundEast, InputEastboundNorth, InputEastboundSouth,
                            InputWestboundWest, InputWestboundNorth, InputWestboundSouth,
                            InputVehicleTopSpeed, InputVehicleReactionTime, InputVehicleStationaryDistance,
                            InputMaximumWaitTimeWeight, InputAverageWaitTimeWeight, InputMaximumQueueLengthWeight):
    connection, cursor = getDatabaseConnection()

    if connection is None or cursor is None:
        print("Failed to connect to the database.")
        return []
    
    try:
        cursor.execute("""
            SELECT insertModelTrafficFlow(%s, %s,
            %s, %s, %s,
            %s, %s, %s,
            %s, %s, %s,
            %s, %s, %s,
            %s, %s, %s,
            %s, %s, %s)
            """, (
            InputModelName, InputSimulationTime,
            InputNorthboundNorth, InputNorthboundEast, InputNorthboundWest, 
            InputSouthboundSouth, InputSouthboundEast, InputSouthboundWest,
            InputEastboundEast, InputEastboundNorth, InputEastboundSouth,
            InputWestboundWest, InputWestboundNorth, InputWestboundSouth,
            InputVehicleTopSpeed, InputVehicleReactionTime, InputVehicleStationaryDistance,
            InputMaximumWaitTimeWeight, InputAverageWaitTimeWeight, InputMaximumQueueLengthWeight
        ))

        connection.commit()
    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
    finally:
        closeDatabaseConnection(connection, cursor)

# Retrieve all model names
def retrieveAllModelNames():
    connection, cursor = getDatabaseConnection()

    if connection is None or cursor is None:
        print("Failed to connect to the database.")
        return []
    
    try:
        cursor.execute("SELECT * FROM retrieveAllModelNames();")

        allModelInformation = cursor.fetchall()

        return allModelInformation
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        closeDatabaseConnection(connection, cursor)