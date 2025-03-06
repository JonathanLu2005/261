import psycopg2

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

        connection.commit()
    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
    finally:
        closeDatabaseConnection(connection, cursor)

# Retrieve all model names
def retrieveAllModelNames(InputUserID):
    connection, cursor = getDatabaseConnection()

    if connection is None or cursor is None:
        print("Failed to connect to the database.")
        return []
    
    try:
        cursor.execute("SELECT * FROM retrieveAllModelNames(%s);", (InputUserID,))

        allModelInformation = cursor.fetchall()

        return allModelInformation
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        closeDatabaseConnection(connection, cursor)

# Insert junction configurations data
def insertJunctionConfigurationsData(InputJunctionName, InputNumberOfLanes, InputJunctionSideLength,
                                     InputPedestrianCrossingAdded, InputPedestrianCrossingDuration, InputPedestrianRequestsPerHour,
                                     InputNorthboundOrder, InputSouthboundOrder, InputEastboundOrder, InputWestboundOrder,
                                     InputNorthboundGreenLightDuration, InputSouthboundGreenLightDuration, InputWestboundGreenLightDuration, InputEastboundGreenLightDuration,
                                     InputLeftTurnLane, InputRightTurnLane,
                                     InputSpecialLane, InputSpecialLaneRatio,
                                     InputModelID):
    connection, cursor = getDatabaseConnection()

    if connection is None or cursor is None:
        print("Failed to connect to the database.")
        return []
    
    try:
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

        connection.commit()
    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
    finally:
        closeDatabaseConnection(connection, cursor)

# Retrieve all junctions
def retrieveAllModelJunctions(InputModelID):
    connection, cursor = getDatabaseConnection()

    if connection is None or cursor is None:
        print("Failed to connect to the database.")
        return []

    try:
        # Execute the function call with the provided modelid
        cursor.execute("SELECT * FROM retrieveAllModelJunctions(%s);", (InputModelID,))

        # Fetch all results from the function call
        allJunctionInformation = cursor.fetchall()

        return allJunctionInformation
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        # Make sure to close the connection properly
        closeDatabaseConnection(connection, cursor)

# Retrieve data for simulation
def retrieveSimulationData(InputModelID):
    connection, cursor = getDatabaseConnection()

    if connection is None or cursor is None:
        print("Failed to connect to the database.")
        return []

    try:
        # Execute the function call with the provided modelid
        cursor.execute("SELECT * FROM dataForSimulation(%s);", (InputModelID,))  

        modelSimulationData = cursor.fetchall()
        
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

        modelSimulationDataHashmap = dict(zip(modelKeys, modelSimulationData[0]))

        print("database model data hashmap")
        print(modelSimulationDataHashmap)

        return modelSimulationDataHashmap
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        closeDatabaseConnection(connection, cursor)

# Insert data to junction performance
def insertJunctionPerformance(InputNorthMaxWait, InputNorthAverageWait, InputNorthMaxQueue, InputNorthTotal,
                            InputSouthMaxWait, InputSouthAverageWait, InputSouthMaxQueue, InputSouthTotal,
                            InputEastMaxWait, InputEastAverageWait, InputEastMaxQueue, InputEastTotal,
                            InputWestMaxWait, InputWestAverageWait, InputWestMaxQueue, InputWestTotal,
                            InputJunctionID):
    connection, cursor = getDatabaseConnection()

    if connection is None or cursor is None:
        print("Failed to connect to the database.")
        return []
    
    try:
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
        
        connection.commit()
    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
    finally:
        closeDatabaseConnection(connection, cursor)

# Retrieve data from junction performance
def retrieveJunctionPerformance(InputJunctionID):
    connection, cursor = getDatabaseConnection()

    if connection is None or cursor is None:
        print("Failed to connect to the database.")
        return []
    
    try:
        cursor.execute("SELECT * FROM retrieveJunctionPerformance(%s);", (InputJunctionID,))
        junctionPerformanceData = cursor.fetchall()

        junctionKeys = [
            "InputNorthMaxWait", "InputNorthAverageWait", "InputNorthMaxQueue", "InputNorthTotal",
            "InputSouthMaxWait", "InputSouthAverageWait", "InputSouthMaxQueue", "InputSouthTotal",
            "InputEastMaxWait", "InputEastAverageWait", "InputEastMaxQueue", "InputEastTotal",
            "InputWestMaxWait", "InputWestAverageWait", "InputWestMaxQueue", "InputWestTotal"
        ]
        junctionSimulationDataHashmap = dict(zip(junctionKeys, junctionPerformanceData[0]))

        return junctionSimulationDataHashmap
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        closeDatabaseConnection(connection, cursor)

# Insert user details
def insertUserDetails(InputUsername, InputPassword):
    connection, cursor = getDatabaseConnection()

    if connection is None or cursor is None:
        print("Failed to connect to the database.")
        return [] 
    
    try: 
        cursor.execute(""" 
        SELECT insertUser(%s, %s)
        """, (InputUsername, InputPassword))

        connection.commit()
    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
    finally:
        closeDatabaseConnection(connection, cursor)

# Retrieve user id
def getUserID(InputUsername, InputPassword):
    connection, cursor = getDatabaseConnection()

    if connection is None or cursor is None:
        print("Failed to connect to the database.")
        return []
    
    try: 
        cursor.execute("SELECT * FROM getUserID(%s, %s);", (InputUsername, InputPassword,))
        userID = cursor.fetchall()
        return userID[0][0]
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        closeDatabaseConnection(connection, cursor)