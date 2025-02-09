-- Model Table
CREATE TABLE IF NOT EXISTS ModelTrafficFlow (
    -- Main model info
    ModelID SERIAL PRIMARY KEY,
    ModelName VARCHAR(100) UNIQUE NOT NULL,

    -- How long simulation runs for
    SimulationTime INTEGER UNIQUE NOT NULL,
    SimulationSecondLength FLOAT NOT NULL,

    -- Total VPH from each direction
    NorthboundVPHTotal INTEGER NOT NULL,
    SouthboundVPHTotal INTEGER NOT NULL,
    EastboundVPHTotal INTEGER NOT NULL,
    WestboundVPHTotal INTEGER NOT NULL,

    -- Northbound broken down
    NorthboundNorthVPH INTEGER NOT NULL,
    NorthboundEastVPH INTEGER NOT NULL,
    NorthboundWestVPH INTEGER NOT NULL,

    -- Southbound broken down
    SouthboundSouthVPH INTEGER NOT NULL,
    SouthboundEastVPH INTEGER NOT NULL,
    SouthboundWestVPH INTEGER NOT NULL, 

    -- Eastbound broken down
    EastboundEastVPH INTEGER NOT NULL,
    EastboundNorthVPH INTEGER NOT NULL,
    EastboundSouthVPH INTEGER NOT NULL,

    -- Westbound broken down
    WestboundWestVPH INTEGER NOT NULL,
    WestboundNorthVPH INTEGER NOT NULL,
    WestboundSouthVPH INTEGER NOT NULL,

    -- Vehicle top speed
    VehicleTopSpeed INTEGER NOT NULL,

    -- Vehicle reaction time and stationary distance
    VehicleReactionTime INTEGER NOT NULL,
    VehicleStationaryDistance INTEGER NOT NULL,

    -- Weightings for results
    MaximumWaitTimeWeight FLOAT NOT NULL DEFAULT 0.33,
    AverageWaitTimeWeight FLOAT NOT NULL DEFAULT 0.33,
    MaximumQueueLengthWeight FLOAT NOT NULL DEFAULT 0.33
);

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