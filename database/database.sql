-- Model Table
CREATE TABLE IF NOT EXISTS modeltrafficflow (
    -- Main model info
    modelid SERIAL PRIMARY KEY,
    modelname VARCHAR(100) UNIQUE NOT NULL,
    simulationtime INTEGER NOT NULL,

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

    -- Vehicle length and fluctuation
    vehiclelength FLOAT NOT NULL,
    vehiclelengthfluctuation FLOAT NOT NULL,

    -- Buses and cycles info
    vehicletopspeedspecial INTEGER NOT NULL,
    vehiclelengthspecial FLOAT NOT NULL, 
    vehiclelengthfluctuationspecial FLOAT NOT NULL, 

    -- Buses and cycles vph
    -- Northbound 
    northboundnorthvphspecial INTEGER NOT NULL,
    northboundeastvphspecial INTEGER NOT NULL,
    northboundwestvphspecial INTEGER NOT NULL,

    -- Southbound
    southboundsouthvphspecial INTEGER NOT NULL,
    southboundeastvphspecial INTEGER NOT NULL,
    southboundwestvphspecial INTEGER NOT NULL, 

    -- Eastbound 
    eastboundeastvphspecial INTEGER NOT NULL,
    eastboundnorthvphspecial INTEGER NOT NULL,
    eastboundsouthvphspecial INTEGER NOT NULL,

    -- Westbound 
    westboundwestvphspecial INTEGER NOT NULL,
    westboundnorthvphspecial INTEGER NOT NULL,
    westboundsouthvphspecial INTEGER NOT NULL,

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
                                                InputVehicleLength FLOAT, InputVehicleLengthFluctuation FLOAT, 

                                                InputVehicleTopSpeedSpecial INTEGER, InputVehicleLengthSpecial FLOAT, InputVehicleLengthFluctuationSpecial FLOAT,
                                               
                                                InputNorthboundNorthSpecial INTEGER, InputNorthboundEastSpecial INTEGER, InputNorthboundWestSpecial INTEGER, 
                                                InputSouthboundSouthSpecial INTEGER, InputSouthboundEastSpecial INTEGER, InputSouthboundWestSpecial INTEGER,
                                                InputEastboundEastSpecial INTEGER, InputEastboundNorthSpecial INTEGER, InputEastboundSouthSpecial INTEGER,
                                                InputWestboundWestSpecial INTEGER, InputWestboundNorthSpecial INTEGER, InputWestboundSouthSpecial INTEGER,

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
                                vehiclelength, vehiclelengthfluctuation,

                                vehicletopspeedspecial, vehiclelengthspecial, vehiclelengthfluctuationspecial,

                                northboundnorthvphspecial, northboundeastvphspecial, northboundwestvphspecial, 
                                southboundsouthvphspecial, southboundeastvphspecial, southboundwestvphspecial,
                                eastboundeastvphspecial, eastboundnorthvphspecial, eastboundsouthvphspecial,
                                westboundwestvphspecial, westboundnorthvphspecial, westboundsouthvphspecial,                                

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
    InputVehicleLength, InputVehicleLengthFluctuation, 

    InputVehicleTopSpeedSpecial, InputVehicleLengthSpecial, InputVehicleLengthFluctuationSpecial,

    InputNorthboundNorthSpecial, InputNorthboundEastSpecial, InputNorthboundWestSpecial, 
    InputSouthboundSouthSpecial, InputSouthboundEastSpecial, InputSouthboundWestSpecial,
    InputEastboundEastSpecial, InputEastboundNorthSpecial, InputEastboundSouthSpecial,
    InputWestboundWestSpecial, InputWestboundNorthSpecial, InputWestboundSouthSpecial,

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
CREATE TABLE IF NOT EXISTS junctionconfigurations (
    -- Main junction info
    junctionid SERIAL PRIMARY KEY,
    junctionname VARCHAR(100) UNIQUE NOT NULL,

    -- Number of lanes
    numberoflanes INTEGER NOT NULL,
    junctionsidelength INTEGER NOT NULL,

    -- Pedestrian crossing information
    pedestriancrossingadded BOOLEAN NOT NULL DEFAULT FALSE,
    pedestriancrossingduration INTEGER NOT NULL DEFAULT 0,
    pedestriancrossingrequestsperhour INTEGER NOT NULL DEFAULT 0,

    -- Order of traffic lights sequencing
    northboundorder INTEGER NOT NULL,
    southboundorder INTEGER NOT NULL,
    eastboundorder INTEGER NOT NULL,
    westboundorder INTEGER NOT NULL,

    -- How long each traffic light runs for
    northboundgreenlightduration INTEGER NOT NULL,
    southboundgreenlightduration INTEGER NOT NULL,
    westboundgreenlightduration INTEGER NOT NULL,
    eastboundgreenlightduration INTEGER NOT NULL,

    -- Other lanes
    leftturnlane BOOLEAN NOT NULL DEFAULT FALSE,
    rightturnlane BOOLEAN NOT NULL DEFAULT FALSE,
    speciallane BOOLEAN NOT NULL DEFAULT FALSE,
    speciallaneratio FLOAT NOT NULL DEFAULT 0,
  
    -- Reference to model for simulation details
    modelid INTEGER NOT NULL REFERENCES modeltrafficflow(modelid)
);

-- Junction - Add data
CREATE OR REPLACE FUNCTION insertJunctionConfigurations(InputJunctionName VARCHAR, InputNumberOfLanes INTEGER, InputJunctionSideLength INTEGER,
                                                        InputPedestrianCrossingAdded BOOLEAN, InputPedestrianCrossingDuration INTEGER, InputPedestrianRequestsPerHour INTEGER,
                                                        InputNorthboundOrder INTEGER, InputSouthboundOrder INTEGER, InputEastboundOrder INTEGER, InputWestboundOrder INTEGER,
                                                        InputNorthboundGreenLightDuration INTEGER, InputSouthboundGreenLightDuration INTEGER, InputWestboundGreenLightDuration INTEGER, InputEastboundGreenLightDuration INTEGER,
                                                        InputLeftTurnLane BOOLEAN, InputRightTurnLane BOOLEAN,
                                                        InputSpecialLane BOOLEAN, InputSpecialLaneRatio FLOAT,
                                                        InputModelID INTEGER)
                                                        RETURNS VOID AS $$
BEGIN 
    INSERT INTO junctionconfigurations(junctionname, numberoflanes, junctionsidelength,
                                        pedestriancrossingadded, pedestriancrossingduration, pedestriancrossingrequestsperhour,
                                        northboundorder, southboundorder, eastboundorder, westboundorder,
                                        northboundgreenlightduration, southboundgreenlightduration, westboundgreenlightduration, eastboundgreenlightduration,
                                        leftturnlane, rightturnlane,
                                        speciallane, speciallaneratio,
                                        modelid) 
    VALUES(InputJunctionName, InputNumberOfLanes, InputJunctionSideLength,
    InputPedestrianCrossingAdded, InputPedestrianCrossingDuration, InputPedestrianRequestsPerHour,
    InputNorthboundOrder, InputSouthboundOrder, InputEastboundOrder, InputWestboundOrder,
    InputNorthboundGreenLightDuration, InputSouthboundGreenLightDuration, InputEastboundGreenLightDuration, InputWestboundGreenLightDuration,
    InputLeftTurnLane, InputRightTurnLane,
    InputSpecialLane, InputSpecialLaneRatio,
    InputModelID);
END;
$$ LANGUAGE plpgsql;

-- Junction - Retrieve data 
CREATE OR REPLACE FUNCTION retrieveAllModelJunctions(inputmodelid INTEGER) 
RETURNS TABLE(junctionid INTEGER, junctionname VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT junctionconfigurations.junctionid, junctionconfigurations.junctionname
    FROM junctionconfigurations
    WHERE junctionconfigurations.modelid = inputmodelid;
END;
$$ LANGUAGE plpgsql;

-- Get all data to send to simulation after being added
CREATE OR REPLACE FUNCTION dataForSimulation(inputmodelid INTEGER)
RETURNS TABLE (modelid INTEGER, simulationtime INTEGER,
            northboundvphtotal INTEGER, southboundvphtotal INTEGER, eastboundvphtotal INTEGER, westboundvphtotal INTEGER,
            northboundnorthvph INTEGER, northboundeastvph INTEGER, northboundwestvph INTEGER,
            southboundsouthvph INTEGER, southboundeastvph INTEGER, southboundwestvph INTEGER,
            eastboundeastvph INTEGER, eastboundnorthvph INTEGER, eastboundsouthvph INTEGER,
            westboundwestvph INTEGER, westboundnorthvph INTEGER, westboundsouthvph INTEGER,
            vehicletopspeed INTEGER, vehiclereactiontime INTEGER, vehiclestationarydistance INTEGER,
            vehiclelength FLOAT, vehiclelengthfluctuation FLOAT, 
            vehicletopspeedspecial INTEGER, vehiclelengthspecial FLOAT, vehiclelengthfluctuationspecial FLOAT,
            northboundnorthvphspecial INTEGER, northboundeastvphspecial INTEGER, northboundwestvphspecial INTEGER,
            southboundsouthvphspecial INTEGER, southboundeastvphspecial INTEGER, southboundwestvphspecial INTEGER,
            eastboundeastvphspecial INTEGER, eastboundnorthvphspecial INTEGER, eastboundsouthvphspecial INTEGER, 
            westboundwestvphspecial INTEGER, westboundnorthvphspecial INTEGER, westboundsouthvphspecial INTEGER,
            maximumwaittimeweight FLOAT, averagewaittimeweight FLOAT, maximumqueuelengthweight FLOAT)
            AS $$
BEGIN
    RETURN QUERY
    SELECT modeltrafficflow.modelid, modeltrafficflow.simulationtime,
        modeltrafficflow.northboundvphtotal, modeltrafficflow.southboundvphtotal, modeltrafficflow.eastboundvphtotal, modeltrafficflow.westboundvphtotal,
        modeltrafficflow.northboundnorthvph, modeltrafficflow.northboundeastvph, modeltrafficflow.northboundwestvph,
        modeltrafficflow.southboundsouthvph, modeltrafficflow.southboundeastvph, modeltrafficflow.southboundwestvph,
        modeltrafficflow.eastboundeastvph, modeltrafficflow.eastboundnorthvph, modeltrafficflow.eastboundsouthvph,
        modeltrafficflow.westboundwestvph, modeltrafficflow.westboundnorthvph, modeltrafficflow.westboundsouthvph,
        modeltrafficflow.vehicletopspeed, modeltrafficflow.vehiclereactiontime, modeltrafficflow.vehiclestationarydistance,
        modeltrafficflow.vehiclelength, modeltrafficflow.vehiclelengthfluctuation,
        modeltrafficflow.vehicletopspeedspecial, modeltrafficflow.vehiclelengthspecial, modeltrafficflow.vehiclelengthfluctuationspecial,
        modeltrafficflow.northboundnorthvphspecial, modeltrafficflow.northboundeastvphspecial, modeltrafficflow.northboundwestvphspecial,
        modeltrafficflow.southboundsouthvphspecial, modeltrafficflow.southboundeastvphspecial, modeltrafficflow.southboundwestvphspecial,
        modeltrafficflow.eastboundeastvphspecial, modeltrafficflow.eastboundnorthvphspecial, modeltrafficflow.eastboundsouthvphspecial,
        modeltrafficflow.westboundwestvphspecial, modeltrafficflow.westboundnorthvphspecial, modeltrafficflow.westboundsouthvphspecial,
        modeltrafficflow.maximumwaittimeweight, modeltrafficflow.averagewaittimeweight, modeltrafficflow.maximumqueuelengthweight
    FROM modeltrafficflow 
    WHERE modeltrafficflow.modelid = inputmodelid;
END;
$$ LANGUAGE plpgsql;

-- Junction Performance Table
CREATE TABLE IF NOT EXISTS junctionperformance (
    -- Main junction performance info
    junctionperformanceid SERIAL PRIMARY KEY,
    --overalljunctionscore FLOAT NOT NULL,

    -- North results
    northmaximumwaittime INTEGER NOT NULL,
    northaveragewaittime INTEGER NOT NULL,
    northmaximumqueuelength INTEGER NOT NULL,
    northtotalvehiclespassed INTEGER NOT NULL,

    -- South results
    southmaximumwaittime INTEGER NOT NULL,
    southaveragewaittime INTEGER NOT NULL,
    southmaximumqueuelength INTEGER NOT NULL,
    southtotalvehiclespassed INTEGER NOT NULL,

    -- East results
    eastmaximumwaittime INTEGER NOT NULL,
    eastaveragewaittime INTEGER NOT NULL,
    eastmaximumqueuelength INTEGER NOT NULL,
    easttotalvehiclespassed INTEGER NOT NULL,

    -- West results
    westmaximumwaittime INTEGER NOT NULL,
    westaveragewaittime INTEGER NOT NULL,
    westmaximumqueuelength INTEGER NOT NULL,
    westtotalvehiclespassed INTEGER NOT NULL,

    -- Refer to what junction performance belongs to
    junctionid INTEGER NOT NULL REFERENCES junctionconfigurations(junctionid)
);

-- Insert into junction performance 
CREATE OR REPLACE FUNCTION insertJunctionPerformance(InputNorthMaxWait INTEGER, InputNorthAverageWait INTEGER, InputNorthMaxQueue INTEGER, InputNorthTotal INTEGER,
                                                    InputSouthMaxWait INTEGER, InputSouthAverageWait INTEGER, InputSouthMaxQueue INTEGER, InputSouthTotal INTEGER,
                                                    InputEastMaxWait INTEGER, InputEastAverageWait INTEGER, InputEastMaxQueue INTEGER, InputEastTotal INTEGER,
                                                    InputWestMaxWait INTEGER, InputWestAverageWait INTEGER, InputWestMaxQueue INTEGER, InputWestTotal INTEGER,
                                                    InputJunctionID INTEGER)
                                                    RETURNS VOID AS $$
BEGIN 
    INSERT INTO junctionperformance(northmaximumwaittime, northaveragewaittime, northmaximumqueuelength, northtotalvehiclespassed,
                                    southmaximumwaittime, southaveragewaittime, southmaximumqueuelength, southtotalvehiclespassed,
                                    eastmaximumwaittime, eastaveragewaittime, eastmaximumqueuelength, easttotalvehiclespassed,
                                    westmaximumwaittime, westaveragewaittime, westmaximumqueuelength, westtotalvehiclespassed,
                                    junctionid)
    VALUES(InputNorthMaxWait, InputNorthAverageWait, InputNorthMaxQueue, InputNorthTotal,
        InputSouthMaxWait, InputSouthAverageWait, InputSouthMaxQueue, InputSouthTotal,
        InputEastMaxWait, InputEastAverageWait, InputEastMaxQueue, InputEastTotal,
        InputWestMaxWait, InputWestAverageWait, InputWestMaxQueue, InputWestTotal,
        InputJunctionID);
END;
$$ LANGUAGE plpgsql;

-- Get junction performance data
CREATE OR REPLACE FUNCTION retrieveJunctionPerformance(InputJunctionID INTEGER)
RETURNS TABLE (
    northmaximumwaittime INTEGER, northaveragewaittime INTEGER, northmaximumqueuelength INTEGER, northtotalvehiclespassed INTEGER,
    southmaximumwaittime INTEGER, southaveragewaittime INTEGER, southmaximumqueuelength INTEGER, southtotalvehiclespassed INTEGER,
    eastmaximumwaittime INTEGER, eastaveragewaittime INTEGER, eastmaximumqueuelength INTEGER, easttotalvehiclespassed INTEGER,
    westmaximumwaittime INTEGER, westaveragewaittime INTEGER, westmaximumqueuelength INTEGER, westtotalvehiclespassed INTEGER
) AS
$$
BEGIN
    RETURN QUERY
    SELECT 
        northmaximumwaittime, northaveragewaittime, northmaximumqueuelength, northtotalvehiclespassed,
        southmaximumwaittime, southaveragewaittime, southmaximumqueuelength, southtotalvehiclespassed,
        eastmaximumwaittime, eastaveragewaittime, eastmaximumqueuelength, easttotalvehiclespassed,
        westmaximumwaittime, westaveragewaittime, westmaximumqueuelength, westtotalvehiclespassed
    FROM junctionperformance
    WHERE junctionid = InputJunctionID;
END;
$$ LANGUAGE plpgsql;