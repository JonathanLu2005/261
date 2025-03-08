# Flask for the web framework
from flask import Flask, render_template, request, jsonify, redirect, url_for, send_file, send_from_directory
import os
# Enum for directions for the model
from enum import IntEnum
# Importing inbuilt database method to retrieve and insert data
from database.database import (
    insertModelTrafficFlowData,
    retrieveAllModelNames,
    insertJunctionConfigurationsData,
    retrieveAllModelJunctions,
    retrieveSimulationData,
    insertJunctionPerformance,
    insertUserDetails,
    getUserID,
    retrieveLatestJunctionID
)
# Importing whats required for the simulation code to run
from model.TrafficControl import TrafficControl, Direction
import simpy
from model.Results import ( 
    runModel
)

# Global variable holds the ID of the user to fetch the correct models and junctions belonging to the user
currentUserID = None

# Create web app
app = Flask(__name__)

# Model page - returns model page
@app.route("/modelPage", methods=["GET"])
def modelPage():
    return render_template("modelPage.html")

# Show models to frontend
@app.route("/api/models", methods=["GET"])
def getAllModels():
    # Retrieve all of the names of the models the user has
    AllModels = retrieveAllModelNames(currentUserID)

    if not AllModels:
        return jsonify([])

    # Create a hashmap with the model id and model names
    CurrentModels = [
        {"id": ModelID, "name": ModelName}
        for ModelID, ModelName in AllModels
    ]

    # Return to the frontend to show
    return jsonify(CurrentModels)

# Add model to model page
@app.route('/addModel', methods=["POST"])
def addModel():
    # Receive the model data sent from the user
    modelData = request.json 

    if not modelData or 'name' not in modelData: 
        return jsonify({"Error": "Invalid Data"}), 400 
    
    # Holds all of the model info after being parsed and converted to the correct data type
    ModelInformation = []

    # Data from the frontend with these keys needs to be converted to float values
    floatKeys = ["maxWaitTimeWeight", "averageWaitTimeWeight", "maxQueueLengthWeight",
                "vehicleLength", "vehicleLengthFluctuation",
                "vehicleLengthSpecial", "vehicleLengthFluctuationSpecial"
                ]

    # Clean the data received from the users (converting them to the right data types)
    for key, value in modelData.items():
        if key == "name":
            ModelInformation.append(value)
        elif key in floatKeys:
            ModelInformation.append(float(value))
        else:
            ModelInformation.append(int(value))

    # Append user id to the model information
    ModelInformation.append(currentUserID)

    # With model information, able to insert all of this into the database
    insertModelTrafficFlowData(*ModelInformation)

    # After adding the new model, will then return the new models
    return getAllModels()

# Junction page - returns the junction page
@app.route("/junctionPage", methods=["GET"])
def junctionPage():
    return render_template("junctionPage.html")

# Show the users junctions to frontend
@app.route("/api/junctions", methods=["GET"])
def getAllJunctions():
    # Retrieve the model id from the frontend to get the junctions that belongs to the right model
    modelId = request.args.get("modelId") 
    if not modelId:
        return jsonify({"Error": "Missing modelId"}), 400

    # Get all junctions belonging to that specific model
    AllJunctions = retrieveAllModelJunctions(modelId)

    if not AllJunctions:
        return jsonify([])

    # Convert the data into a hashmap
    CurrentJunctions = [
        {"junctionid": JunctionID, "junctionname": JunctionName}
        for JunctionID, JunctionName in AllJunctions
    ]

    # To return it to show to frontend
    return jsonify(CurrentJunctions)

# Add junction 
@app.route("/addJunction", methods=["POST"])
def addJunction():
    # Receive the junction data from the user
    junctionData = request.json
    if not junctionData:
        return jsonify({"Error": "Invalid Data"}), 400

    # Array to hold the junction data after being parsed and converted to the right data types
    junctionInformation = []

    # Specific keys with data that needs to be converted to boolean
    convertToBoolean = ["pedestrianCrossingAdded", "leftTurnLane", "rightTurnLane", "specialLane"]

    # Converting the data to its right data type in junctionData
    for configuration in convertToBoolean:
        if junctionData[configuration].lower() == "yes":
            junctionData[configuration] = True 
        else:
            junctionData[configuration] = False 

            if configuration == "specialLane":
                junctionData["specialLaneRatio"] = 0

    # Then cleaning and converting all data to its right data type in junctionInformation to be used with database
    for key, value in junctionData.items():
        if key in ["junctionName", "pedestrianCrossingAdded", "leftTurnLane", "rightTurnLane", "specialLane"]:
            junctionInformation.append(value)
        elif key in ["pedestrianCrossingDuration", "pedestrianCrossingRequests"] and value == "":
            junctionInformation.append(0)
            junctionData[key] = 0 
        elif key == "specialLaneRatio":
            junctionInformation.append(float(value))
        else:
            junctionInformation.append(int(value))

    # Insert into the database
    insertJunctionConfigurationsData(*junctionInformation)

    # Once junction is added, it is time to start simulating it

    # Retrieve model id to get the correct model data
    modelId = int(junctionData["modelId"])
    modelData = retrieveSimulationData(modelId)

    # Convert the ordering of traffic lights with enum
    class Direction(IntEnum):
        North = int(junctionData["northboundOrder"]), 
        East = int(junctionData["eastboundOrder"]), 
        South = int(junctionData["southboundOrder"]), 
        West = int(junctionData["westboundOrder"])

    # Calls run model to simulate the traffic and junction
    simulationResults = runModel(int(junctionData["junctionSideLength"]),
        modelData["SimulationTime"], modelData["VehicleTopSpeed"], modelData["VehicleLength"], modelData["VehiceLengthFluctuation"],
        modelData["VehicleStationaryDistance"], modelData["VehicleReactionTime"],
        int(junctionData["junctionLanes"]), 
        [
            [modelData["NorthboundNorthVph"], modelData["NorthboundEastVph"], modelData["NorthboundWestVph"]],
            [modelData["EastboundEastVph"], modelData["EastboundSouthVph"], modelData["EastboundNorthVph"]],
            [modelData["SouthboundSouthVph"], modelData["SouthboundWestVph"], modelData["SouthboundEastVph"]],
            [modelData["WestboundWestVph"], modelData["WestboundNorthVph"], modelData["WestboundSouthVph"]]
        ],
        junctionData["leftTurnLane"], junctionData["rightTurnLane"],
        junctionData["pedestrianCrossingAdded"], int(junctionData["pedestrianCrossingDuration"]), int(junctionData["pedestrianCrossingRequests"]),
        [
            Direction.North,
            Direction.East,
            Direction.South,
            Direction.West
        ],
        [
            int(junctionData["northboundDuration"]), 
            int(junctionData["eastboundDuration"]), 
            int(junctionData["southboundDuration"]), 
            int(junctionData["westboundDuration"])
        ],
        modelData["VehicleLengthSpecial"], modelData["VehicleTopSpeedSpecial"], 
        modelData["VehicleLengthFluctuationSpecial"], junctionData["specialLane"], 
        float(junctionData["specialLaneRatio"]),
        [
            [modelData["NorthboundNorthVphSpecial"], modelData["NorthboundEastVphSpecial"], modelData["NorthboundWestVphSpecial"]],
            [modelData["EastboundEastVphSpecial"], modelData["EastboundSouthVphSpecial"], modelData["EastboundNorthVphSpecial"]],
            [modelData["SouthboundSouthVphSpecial"], modelData["SouthboundWestVphSpecial"], modelData["SouthboundEastVphSpecial"]],
            [modelData["WestboundWestVphSpecial"], modelData["WestboundNorthVphSpecial"], modelData["WestboundSouthVphSpecial"]]
        ],
    )

    junctionID = retrieveLatestJunctionID()

    # Receive the results of the junction and insert into database
    insertJunctionPerformance(
        float(simulationResults.northMaxWaitingTime), float(simulationResults.northMaxQueueLength), float(simulationResults.northAvgWaitingTime), float(simulationResults.northTotalVehiclesPassed), 
        float(simulationResults.eastMaxWaitingTime), float(simulationResults.eastMaxQueueLength), float(simulationResults.eastAvgWaitingTime), float(simulationResults.eastTotalVehiclesPassed),
        float(simulationResults.southMaxWaitingTime), float(simulationResults.southMaxQueueLength), float(simulationResults.southAvgWaitingTime), float(simulationResults.southTotalVehiclesPassed),
        float(simulationResults.westMaxWaitingTime), float(simulationResults.westMaxQueueLength), float(simulationResults.westAvgWaitingTime), float(simulationResults.westTotalVehiclesPassed),
        junctionID
    )

    # After adding the new junction, call this to show the junctions and the new one to user
    return getAllJunctions()

# Receiving data to create visualisations
@app.route("/api/receiveJunctionData", methods=["POST"])
def receiveJunctionData():
    # Retrieve data from the junction
    data = request.json

    if not data:
        return jsonify({"Error": "No data received"}), 400

    # Get the junction id and model id to retrieve data from database and create visualisations
    modelID = data.get("modelId")
    junctionID = data.get("junctionId")

    if not modelID or not junctionID:
        return jsonify({"Error": "Missing modelId or junctionId"}), 400

    # INTEGRATE GRAPHIC CODE HERE, THE ABOVE PROVIDES THE JUNCTION AND MODEL ID NEEDED

    # Generates image and is stored in static, to show to frontend when user clicks on junction and want to see performance visualisations
    return jsonify({"Message": "Data received successfully"}), 200

# Help page - returns the help section
@app.route("/helpPage", methods=["POST", "GET"])
def helpPage():
    return render_template("helpPage.html")

# Account page
@app.route("/", methods=["POST", "GET"])
def account():
    # If the users logging in or signing up
    if request.method == "POST":
        # Get the action, and username and password
        action = request.form.get('action')
        username = request.form.get('username')
        password = request.form.get('password')

        # If they're signing up, update this into the database
        if action == 'signup':
            insertUserDetails(username, password)

        # Get the id of the user after logging in / creating an account and globalise it to refer to later on
        userID = getUserID(username, password)
        global currentUserID
        currentUserID = userID

        # Show the user the model page
        return redirect(url_for('modelPage'))

    # Show the account page
    return render_template("account.html")

# Ensures web app runs
if __name__ == "__main__":
    app.run(debug=True)