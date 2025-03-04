from flask import Flask, render_template, request, jsonify, redirect, url_for
from enum import IntEnum
from database.database import (
    insertModelTrafficFlowData,
    retrieveAllModelNames,
    insertJunctionConfigurationsData,
    retrieveAllModelJunctions,
    retrieveSimulationData,
    insertJunctionPerformance,
    insertUserDetails,
    getUserID
)

currentUserID = None

# Create web app
app = Flask(__name__)

# Model page
@app.route("/modelPage", methods=["GET"])
def modelPage():
    print(currentUserID)
    return render_template("modelPage.html")

# Show models to frontend
@app.route("/api/models", methods=["GET"])
def getAllModels():
    AllModels = retrieveAllModelNames()

    if not AllModels:
        return jsonify([])

    CurrentModels = [
        {"id": ModelID, "name": ModelName}
        for ModelID, ModelName in AllModels
    ]
    return jsonify(CurrentModels)

# Add model to model page
@app.route('/addModel', methods=["POST"])
def addModel():
    modelData = request.json 

    print(modelData)

    if not modelData or 'name' not in modelData: 
        return jsonify({"Error": "Invalid Data"}), 400 
    
    ModelInformation = []

    floatKeys = ["maxWaitTimeWeight", "averageWaitTimeWeight", "maxQueueLengthWeight",
                "vehicleLength", "vehicleLengthFluctuation",
                "vehicleLengthSpecial", "vehicleLengthFluctuationSpecial"
                ]

    for key, value in modelData.items():
        if key == "name":
            ModelInformation.append(value)
        elif key in floatKeys:
            ModelInformation.append(float(value))
        else:
            ModelInformation.append(int(value))

    insertModelTrafficFlowData(*ModelInformation)
    return getAllModels()

# Show junction page with model information
@app.route("/junctionPage", methods=["GET"])
def junctionPage():
    return render_template("junctionPage.html")

# Show junctions to frontend
@app.route("/api/junctions", methods=["GET"])
def getAllJunctions():
    modelId = request.args.get("modelId")  # Get modelId from query parameters
    if not modelId:
        return jsonify({"Error": "Missing modelId"}), 400

    AllJunctions = retrieveAllModelJunctions(modelId)

    if not AllJunctions:
        return jsonify([])

    CurrentJunctions = [
        {"junctionid": JunctionID, "junctionname": JunctionName}
        for JunctionID, JunctionName in AllJunctions
    ]

    return jsonify(CurrentJunctions)

# Add junction with model ID
@app.route("/addJunction", methods=["POST"])
def addJunction():
    junctionData = request.json

    print(junctionData)
    print("Received junction data:", junctionData)  # Add this line for debugging

    if not junctionData:
        print("Error: Invalid data received.")  # Debugging
        return jsonify({"Error": "Invalid Data"}), 400

    junctionInformation = []

    convertToBoolean = ["pedestrianCrossingAdded", "leftTurnLane", "rightTurnLane", "specialLane"]

    for configuration in convertToBoolean:
        if junctionData[configuration].lower() == "yes":
            junctionData[configuration] = True 
        else:
            junctionData[configuration] = False 

            if configuration == "specialLane":
                junctionData["specialLaneRatio"] = 0



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
    modelId = request.args.get("modelId") 
    modelData = retrieveSimulationData(modelId)

    class Direction(IntEnum):
        North = junctionData["northboundOrder"], 
        East = junctionData["eastboundOrder"], 
        South = junctionData["southboundOrder"], 
        West = junctionData["westboundOrder"]

    """
    simulationResults = runModel(junctionData["junctionSideLength"],
        modelData["SimulationTime"], modelData["VehicleTopSpeed"], modelData["VehicleLength"], modelData["VehiceLengthFluctuation"],
        modelData["VehicleStationaryDistance"], modelData["VehicleReactionTime"],
        junctionData["junctionLanes"], 
        [
            [modelData["NorthboundNorthVph"], modelData["NorthboundEastVph"], modelData["NorthboundWestVph"]],
            [modelData["EastboundEastVph"], modelData["EastboundSouthVph"], modelData["EastboundNorthVph"]],
            [modelData["SouthboundSouthVph"], modelData["SouthboundWestVph"], modelData["SouthboundEastVph"]],
            [modelData["WestboundWestVph"], modelData["WestboundNorthVph"], modelData["WestboundSouthVph"]]
        ],
        junctionData["leftTurnLane"], junctionData["rightTurnLane"],
        junctionData["pedestrianCrossingAdded"], junctionData["pedestrianCrossingDuration"], junctionData["pedestrianCrossingRequests"],
        [
            Direction.North,
            Direction.East,
            Direction.South,
            Direction.West
        ],
        [
            junctionData["northboundDuration"], 
            junctionData["eastboundDuration"], 
            junctionData["southboundDuration"], 
            junctionData["westboundDuration"]
        ],
        modelData["VehicleLengthSpecial"], modelData["VehicleTopSpeedSpecial"], 
        modelData["VehicleLengthFluctuationSpecial"], junctionData["specialLane"], 
        junctionData["specialLaneRatio"],
        [
            [modelData["NorthboundNorthVphSpecial"], modelData["NorthboundEastVphSpecial"], modelData["NorthboundWestVphSpecial"]],
            [modelData["EastboundEastVphSpecial"], modelData["EastboundSouthVphSpecial"], modelData["EastboundNorthVphSpecial"]],
            [modelData["SouthboundSouthVphSpecial"], modelData["SouthboundWestVphSpecial"], modelData["SouthboundEastVphSpecial"]],
            [modelData["WestboundWestVphSpecial"], modelData["WestboundNorthVphSpecial"], modelData["WestboundSouthVphSpecial"]]
        ],
    )

    # insert simulation results - get results from above and store it for visualisations section
    insertJunctionPerformance(
        simulationResults.northMaxWaitingTime, simulationResults.northMaxQueueLength, simulationResults.northAvgWaitingTime, simulationResults.northTotalVehiclesPassed, 
        simulationResults.eastMaxWaitingTime, simulationResults.eastMaxQueueLength, simulationResults.eastAvgWaitingTime, simulationResults.eastTotalVehiclesPassed,
        simulationResults.southMaxWaitingTime, simulationResults.southMaxQueueLength, simulationResults.southAvgWaitingTime, simulationResults.southTotalVehiclesPassed,
        simulationResults.westMaxWaitingTime, simulationResults.westMaxQueueLength, simulationResults.westAvgWaitingTime, simulationResults.westTotalVehiclesPassed,
        junctionData["junctionid"]
    )
    """

    return getAllJunctions()



# Help page
@app.route("/helpPage", methods=["POST", "GET"])
def helpPage():
    return render_template("helpPage.html")

# Help page
@app.route("/", methods=["POST", "GET"])
def account():
    if request.method == "POST":
        action = request.form.get('action')
        username = request.form.get('username')
        password = request.form.get('password')

        print(action)
        print(username)
        print(password)
            
        if action == 'signup':
            insertUserDetails(username, password)

        userID = getUserID(username, password)
        print(userID)
        global currentUserID
        currentUserID = userID

        return redirect(url_for('modelPage'))

    return render_template("account.html")

# Ensures framework works
if __name__ == "__main__":
    app.run(debug=True)