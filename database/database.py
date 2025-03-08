import psycopg2

# Connection parameters for render cloud database
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

# Insert model traffic flow data
def insertModelTrafficFlowData(InputModelName, InputSimulationTime,
                            InputNorthboundNorth, InputNorthboundEast, InputNorthboundWest, 
                            InputSouthboundSouth, InputSouthboundEast, InputSouthboundWest,
                            InputEastboundEast, InputEastboundNorth, InputEastboundSouth,
                            InputWestboundWest, InputWestboundNorth, InputWestboundSouth,
                            InputVehicleTopSpeed, InputVehicleReactionTime, InputVehicleStationaryDistance,
                            InputVehicleLength, InputVehicleLengthFluctuation, 
                            InputVehicleTopSpeedSpecial, InputVehicleLengthSpecial, InputVehicleLengthFluctuationSpecial,
                            InputNorthboundNorthSpecial, InputNorthboundEastSpecial, InputNorthboundWestSpecial, 
                            InputSouthboundSouthSpecial, InputSouthboundEastSpecial, InputSouthboundWestSpecial,
                            InputEastboundEastSpecial, InputEastboundNorthSpecial, InputEastboundSouthSpecial,
                            InputWestboundWestSpecial, InputWestboundNorthSpecial, InputWestboundSouthSpecial,
                            InputMaximumWaitTimeWeight, InputAverageWaitTimeWeight, InputMaximumQueueLengthWeight,
                            InputUserID):
    # Get connection and cursor
    connection, cursor = getDatabaseConnection()

    if connection is None or cursor is None:
        print("Failed to connect to the database.")
        return []
    
    try:
        # Call SQL method and insert model data
        cursor.execute("""
            SELECT insertModelTrafficFlow(%s, %s,
            %s, %s, %s,
            %s, %s, %s,
            %s, %s, %s,
            %s, %s, %s,
            %s, %s, %s,
            %s, %s, 
            %s, %s, %s,
            %s, %s, %s,
            %s, %s, %s,
            %s, %s, %s,
            %s, %s, %s,          
            %s, %s, %s, 
            %s)
            """, (
            InputModelName, InputSimulationTime,
            InputNorthboundNorth, InputNorthboundEast, InputNorthboundWest, 
            InputSouthboundSouth, InputSouthboundEast, InputSouthboundWest,
            InputEastboundEast, InputEastboundNorth, InputEastboundSouth,
            InputWestboundWest, InputWestboundNorth, InputWestboundSouth,
            InputVehicleTopSpeed, InputVehicleReactionTime, InputVehicleStationaryDistance,
            InputVehicleLength, InputVehicleLengthFluctuation, 
            InputVehicleTopSpeedSpecial, InputVehicleLengthSpecial, InputVehicleLengthFluctuationSpecial,
            InputNorthboundNorthSpecial, InputNorthboundEastSpecial, InputNorthboundWestSpecial, 
            InputSouthboundSouthSpecial, InputSouthboundEastSpecial, InputSouthboundWestSpecial,
            InputEastboundEastSpecial, InputEastboundNorthSpecial, InputEastboundSouthSpecial,
            InputWestboundWestSpecial, InputWestboundNorthSpecial, InputWestboundSouthSpecial,
            InputMaximumWaitTimeWeight, InputAverageWaitTimeWeight, InputMaximumQueueLengthWeight,
            InputUserID
        ))

        # Add to database
        connection.commit()
    except Exception as e:
        # Any errors can rollback
        print(f"Error: {e}")
        connection.rollback()
    finally:
        # Close connection
        closeDatabaseConnection(connection, cursor)

# Retrieve all model names
def retrieveAllModelNames(InputUserID):
    # Get connection and cursor
    connection, cursor = getDatabaseConnection()

    if connection is None or cursor is None:
        print("Failed to connect to the database.")
        return []
    
    try:
        # Get all models belonging to the user
        cursor.execute("SELECT * FROM retrieveAllModelNames(%s);", (InputUserID,))

        allModelInformation = cursor.fetchall()

        # Return to app.py to use
        return allModelInformation
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        # Close connection
        closeDatabaseConnection(connection, cursor)

# Insert junction configurations data
def insertJunctionConfigurationsData(InputJunctionName, InputNumberOfLanes, InputJunctionSideLength,
                                     InputPedestrianCrossingAdded, InputPedestrianCrossingDuration, InputPedestrianRequestsPerHour,
                                     InputNorthboundOrder, InputSouthboundOrder, InputEastboundOrder, InputWestboundOrder,
                                     InputNorthboundGreenLightDuration, InputSouthboundGreenLightDuration, InputWestboundGreenLightDuration, InputEastboundGreenLightDuration,
                                     InputLeftTurnLane, InputRightTurnLane,
                                     InputSpecialLane, InputSpecialLaneRatio,
                                     InputModelID):
    # Get connection and cursor
    connection, cursor = getDatabaseConnection()

    if connection is None or cursor is None:
        print("Failed to connect to the database.")
        return []
    
    try:
        # Insert junction design 
        cursor.execute("""
            SELECT insertJunctionConfigurations(%s, %s, %s,
            %s, %s, %s,
            %s, %s, %s, %s,
            %s, %s, %s, %s,
            %s, %s,
            %s, %s,
            %s)
        """, (
            InputJunctionName, InputNumberOfLanes, InputJunctionSideLength,
            InputPedestrianCrossingAdded, InputPedestrianCrossingDuration, InputPedestrianRequestsPerHour,
            InputNorthboundOrder, InputSouthboundOrder, InputEastboundOrder, InputWestboundOrder,
            InputNorthboundGreenLightDuration, InputSouthboundGreenLightDuration, InputWestboundGreenLightDuration, InputEastboundGreenLightDuration,
            InputLeftTurnLane, InputRightTurnLane,
            InputSpecialLane, InputSpecialLaneRatio,
            InputModelID
        ))

        # Add to database
        connection.commit()
    except Exception as e:
        # Any errors can rollback
        print(f"Error: {e}")
        connection.rollback()
    finally:
        # Close connection
        closeDatabaseConnection(connection, cursor)

# Retrieve all junctions
def retrieveAllModelJunctions(InputModelID):
    # Get connection and cursor
    connection, cursor = getDatabaseConnection()

    if connection is None or cursor is None:
        print("Failed to connect to the database.")
        return []

    try:
        # Get model information for given model
        cursor.execute("SELECT * FROM retrieveAllModelJunctions(%s);", (InputModelID,))

        allJunctionInformation = cursor.fetchall()

        # Send to app.py
        return allJunctionInformation
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        # Close connection
        closeDatabaseConnection(connection, cursor)

# Retrieve latest junction ID
def retrieveLatestJunctionID():
    # Get connection and cursor
    connection, cursor = getDatabaseConnection()   

    if connection is None or cursor is None:
        print("Failed to connect to the database.")
        return []

    try:
        # Get latest junction ID
        cursor.execute("SELECT * FROM getLatestJunctionID();")
        latestJunctionID = cursor.fetchone()

        # Send to app.py
        return latestJunctionID[0]
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        # Close connection
        closeDatabaseConnection(connection, cursor)

# Retrieve data for simulation
def retrieveSimulationData(InputModelID):
    # Get connection and cursor
    connection, cursor = getDatabaseConnection()

    if connection is None or cursor is None:
        print("Failed to connect to the database.")
        return []

    try:
        # Get data for simulation to run
        cursor.execute("SELECT * FROM dataForSimulation(%s);", (InputModelID,))  

        modelSimulationData = cursor.fetchall()
        
        # Keys to make a hashmap with the model data to make access easier on app.py
        modelKeys = [
            "ModelID", "SimulationTime",
            "NorthboundVphTotal", "SouthboundVphTotal", "EastboundVphTotal", "WestboundVphTotal",
            "NorthboundNorthVph", "NorthboundEastVph", "NorthboundWestVph",
            "SouthboundSouthVph", "SouthboundEastVph", "SouthboundWestVph",
            "EastboundEastVph", "EastboundNorthVph", "EastboundSouthVph",
            "WestboundWestVph", "WestboundNorthVph", "WestboundSouthVph",
            "VehicleTopSpeed", "VehicleReactionTime", "VehicleStationaryDistance",
            "VehicleLength", "VehiceLengthFluctuation",
            "VehicleTopSpeedSpecial", "VehicleLengthSpecial", "VehicleLengthFluctuationSpecial",
            "NorthboundNorthVphSpecial", "NorthboundEastVphSpecial", "NorthboundWestVphSpecial",
            "SouthboundSouthVphSpecial", "SouthboundEastVphSpecial", "SouthboundWestVphSpecial",
            "EastboundEastVphSpecial", "EastboundNorthVphSpecial", "EastboundSouthVphSpecial",
            "WestboundWestVphSpecial", "WestboundNorthVphSpecial", "WestboundSouthVphSpecial",
            "MaximumWaitTimeWeight", "AverageWaitTimeWeight", "MaximumQueueLengthWeight"
        ]

        # Create hashmap with keys and the model data
        modelSimulationDataHashmap = dict(zip(modelKeys, modelSimulationData[0]))

        # Return to app.py
        return modelSimulationDataHashmap
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        # Close connection and cursor
        closeDatabaseConnection(connection, cursor)

# Insert data to junction performance
def insertJunctionPerformance(InputNorthMaxWait, InputNorthAverageWait, InputNorthMaxQueue, InputNorthTotal,
                            InputSouthMaxWait, InputSouthAverageWait, InputSouthMaxQueue, InputSouthTotal,
                            InputEastMaxWait, InputEastAverageWait, InputEastMaxQueue, InputEastTotal,
                            InputWestMaxWait, InputWestAverageWait, InputWestMaxQueue, InputWestTotal,
                            InputJunctionID):
    # Get connection and cursor
    connection, cursor = getDatabaseConnection()

    if connection is None or cursor is None:
        print("Failed to connect to the database.")
        return []
    
    try:
        # Insert the junction performance to table
        cursor.execute(""" 
            SELECT insertJunctionPerformance(
                %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s)
            """, (InputNorthMaxWait, InputNorthAverageWait, InputNorthMaxQueue, InputNorthTotal,
            InputSouthMaxWait, InputSouthAverageWait, InputSouthMaxQueue, InputSouthTotal,
            InputEastMaxWait, InputEastAverageWait, InputEastMaxQueue, InputEastTotal,
            InputWestMaxWait, InputWestAverageWait, InputWestMaxQueue, InputWestTotal,
            InputJunctionID))
        
        # Add to database
        connection.commit()
    except Exception as e:
        # If error rollback
        print(f"Error: {e}")
        connection.rollback()
    finally:
        # Close connection and cursor
        closeDatabaseConnection(connection, cursor)

# Retrieve data from junction performance
def retrieveJunctionPerformance(InputJunctionID):
    # Get connection and cursor
    connection, cursor = getDatabaseConnection()

    if connection is None or cursor is None:
        print("Failed to connect to the database.")
        return []
    
    try:
        # Retrieve junction performance
        cursor.execute("SELECT * FROM retrieveJunctionPerformance(%s);", (InputJunctionID,))
        junctionPerformanceData = cursor.fetchall()
        
        # Keys to create hashmap with junction performance to make it easier to use in app.py
        junctionKeys = [
            "InputNorthMaxWait", "InputNorthAverageWait", "InputNorthMaxQueue", "InputNorthTotal",
            "InputSouthMaxWait", "InputSouthAverageWait", "InputSouthMaxQueue", "InputSouthTotal",
            "InputEastMaxWait", "InputEastAverageWait", "InputEastMaxQueue", "InputEastTotal",
            "InputWestMaxWait", "InputWestAverageWait", "InputWestMaxQueue", "InputWestTotal"
        ]

        # Create hashmap
        junctionSimulationDataHashmap = dict(zip(junctionKeys, junctionPerformanceData[0]))

        # Return to app.py
        return junctionSimulationDataHashmap
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        # Close connection and cursor
        closeDatabaseConnection(connection, cursor)

# Insert user details
def insertUserDetails(InputUsername, InputPassword):
    # Get connection and cursor
    connection, cursor = getDatabaseConnection()

    if connection is None or cursor is None:
        print("Failed to connect to the database.")
        return [] 
    
    try: 
        # Insert to user table
        cursor.execute(""" 
        SELECT insertUser(%s, %s)
        """, (InputUsername, InputPassword))

        # Add to database
        connection.commit()
    except Exception as e:
        # If error, rollback
        print(f"Error: {e}")
        connection.rollback()
    finally:
        # Close connection and cursor
        closeDatabaseConnection(connection, cursor)

# Retrieve user id
def getUserID(InputUsername, InputPassword):
    # Get connection and cursor
    connection, cursor = getDatabaseConnection()

    if connection is None or cursor is None:
        print("Failed to connect to the database.")
        return []
    
    try: 
        # Get user id given username and password
        cursor.execute("SELECT * FROM getUserID(%s, %s);", (InputUsername, InputPassword,))
        userID = cursor.fetchall()

        # Return user id to app.py
        return userID[0][0]
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        # Close connection and cursor
        closeDatabaseConnection(connection, cursor)