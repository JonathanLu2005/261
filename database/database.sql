-- Model Table
CREATE TABLE IF NOT EXISTS modeltrafficflow (
    -- Main model info
    modelid SERIAL PRIMARY KEY,
    modelname VARCHAR(100) UNIQUE NOT NULL,

    -- How long simulation runs for
    simulationtime INTEGER NOT NULL,
    --SimulationSecondLength FLOAT NOT NULL,

    -- Total VPH from each direction
    northboundvphtotal INTEGER NOT NULL,
    southboundvphtotal INTEGER NOT NULL,
    eastboundvphtotal INTEGER NOT NULL,
    westboundvphtotal INTEGER NOT NULL,

    -- Northbound broken down
    northboundnorthvph INTEGER NOT NULL,
    northboundeastvph INTEGER NOT NULL,
    northboundwestvph INTEGER NOT NULL,

    -- Southbound broken down
    southboundsouthvph INTEGER NOT NULL,
    southboundeastvph INTEGER NOT NULL,
    southboundwestvph INTEGER NOT NULL, 

    -- Eastbound broken down
    eastboundeastvph INTEGER NOT NULL,
    eastboundnorthvph INTEGER NOT NULL,
    eastboundsouthvph INTEGER NOT NULL,

    -- Westbound broken down
    westboundwestvph INTEGER NOT NULL,
    westboundnorthvph INTEGER NOT NULL,
    westboundsouthvph INTEGER NOT NULL,

    -- Vehicle top speed
    vehicletopspeed INTEGER NOT NULL,

    -- Vehicle reaction time and stationary distance
    vehiclereactiontime INTEGER NOT NULL,
    vehiclestationarydistance INTEGER NOT NULL,

    -- Weightings for results
    maximumwaittimeweight FLOAT NOT NULL DEFAULT 0.33,
    averagewaittimeweight FLOAT NOT NULL DEFAULT 0.33,
    maximumqueuelengthweight FLOAT NOT NULL DEFAULT 0.33
);

-- Model - Add data
CREATE OR REPLACE FUNCTION insertModelTrafficFlow(InputModelName VARCHAR, InputSimulationTime INTEGER,

                                                InputNorthboundNorth INTEGER, InputNorthboundEast INTEGER, InputNorthboundWest INTEGER, 
                                                InputSouthboundSouth INTEGER, InputSouthboundEast INTEGER, InputSouthboundWest INTEGER,
                                                InputEastboundEast INTEGER, InputEastboundNorth INTEGER, InputEastboundSouth INTEGER,
                                                InputWestboundWest INTEGER, InputWestboundNorth INTEGER, InputWestboundSouth INTEGER,

                                                InputVehicleTopSpeed INTEGER, InputVehicleReactionTime INTEGER, InputVehicleStationaryDistance INTEGER,
                                               
                                                InputMaximumWaitTimeWeight FLOAT, InputAverageWaitTimeWeight FLOAT, InputMaximumQueueLengthWeight FLOAT)
                                                RETURNS VOID AS $$
BEGIN
    INSERT INTO modeltrafficflow (modelname, simulationtime,
                                northboundvphtotal, southboundvphtotal, eastboundvphtotal, westboundvphtotal,

                                northboundnorthvph, northboundeastvph, northboundwestvph, 
                                southboundsouthvph, southboundeastvph, southboundwestvph,
                                eastboundeastvph, eastboundnorthvph, eastboundsouthvph,
                                westboundwestvph, westboundnorthvph, westboundsouthvph,

                                vehicletopspeed, vehiclereactiontime, vehiclestationarydistance,

                                maximumwaittimeweight, averagewaittimeweight, maximumqueuelengthweight)
    VALUES(InputModelName, InputSimulationTime,

    InputNorthboundNorth + InputNorthboundEast + InputNorthboundWest,
    InputSouthboundSouth + InputSouthboundEast + InputSouthboundWest,
    InputEastboundEast + InputEastboundNorth + InputEastboundSouth,
    InputWestboundWest + InputWestboundNorth + InputWestboundSouth,

    InputNorthboundNorth, InputNorthboundEast, InputNorthboundWest,
    InputSouthboundSouth, InputSouthboundEast, InputSouthboundWest,
    InputEastboundEast, InputEastboundNorth, InputEastboundSouth,
    InputWestboundWest, InputWestboundNorth, InputWestboundSouth,

    InputVehicleTopSpeed, InputVehicleReactionTime, InputVehicleStationaryDistance,

    InputMaximumWaitTimeWeight, InputAverageWaitTimeWeight, InputMaximumQueueLengthWeight);
END;
$$ LANGUAGE plpgsql;

-- Model - Retrieve data 
CREATE OR REPLACE FUNCTION retrieveAllModelNames() RETURNS TABLE(modelid INTEGER, modelname VARCHAR) AS $$
BEGIN 
    RETURN QUERY
    SELECT modeltrafficflow.modelid, modeltrafficflow.modelname FROM modeltrafficflow;
END;
$$ LANGUAGE plpgsql;

-- Junction Configuration Table
CREATE TABLE IF NOT EXISTS JunctionConfigurations (
    -- Main junction info
    JunctionID SERIAL PRIMARY KEY,
    JunctionName VARCHAR(100) UNIQUE NOT NULL,

    -- Number of lanes
    NumberOfLanes INTEGER NOT NULL,

    -- Pedestrian crossing information
    PedestrianCrossingAdded BOOLEAN NOT NULL DEFAULT FALSE,
    PedestrianCrossingDuration INTEGER NOT NULL DEFAULT 0,
    PedestrianCrossingRequestsPerHour INTEGER NOT NULL DEFAULT 0,

    -- Order of traffic lights sequencing
    NorthboundOrder INTEGER NOT NULL,
    SouthboundOrder INTEGER NOT NULL,
    EastboundOrder INTEGER NOT NULL,
    WestboundOrder INTEGER NOT NULL,

    -- How long each traffic light runs for
    NorthboundGreenLightDuration INTEGER NOT NULL,
    SouthboundGreenLightDuration INTEGER NOT NULL,
    WestboundGreenLightDuration INTEGER NOT NULL,
    EastboundGreenLightDuration INTEGER NOT NULL,

    -- Reference to model for simulation details
    ModelID INTEGER NOT NULL REFERENCES ModelTrafficFlow(ModelID)
);

-- Junction Performance Table
CREATE TABLE IF NOT EXISTS JunctionPerformance (
    -- Main junction performance info
    JunctionPerformanceID SERIAL PRIMARY KEY,
    OverallJunctionScore FLOAT NOT NULL,

    -- North results
    NorthMaximumWaitTime INTEGER NOT NULL,
    NorthAverageWaitTime INTEGER NOT NULL,
    NorthMaximumQueueLength INTEGER NOT NULL,

    -- South results
    SouthMaximumWaitTime INTEGER NOT NULL,
    SouthAverageWaitTime INTEGER NOT NULL,
    SouthMaximumQueueLength INTEGER NOT NULL,

    -- East results
    EastMaximumWaitTime INTEGER NOT NULL,
    EastAverageWaitTime INTEGER NOT NULL,
    EastMaximumQueueLength INTEGER NOT NULL,

    -- West results
    WestMaximumWaitTime INTEGER NOT NULL,
    WestAverageWaitTime INTEGER NOT NULL,
    WestMaximumQueueLength INTEGER NOT NULL,

    -- Refer to what junction performance belongs to
    JunctionID INTEGER NOT NULL REFERENCES JunctionConfigurations(JunctionID)
);