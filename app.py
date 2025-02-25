from flask import Flask, render_template, request, jsonify, redirect, url_for
from database.database import (
    insertModelTrafficFlowData,
    retrieveAllModelNames,
    insertJunctionConfigurationsData,
    retrieveAllModelJunctions,
    retrieveSimulationData
)

# Create web app
app = Flask(__name__)

# Model page
@app.route("/", methods=["GET"])
def modelPage():
    print(retrieveSimulationData(27))
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

    if not modelData or 'name' not in modelData: 
        return jsonify({"Error": "Invalid Data"}), 400 
    
    ModelInformation = []

    for key, value in modelData.items():
        if key == "name":
            ModelInformation.append(value)
        elif (key == "maxWaitTimeWeight") or (key == "averageWaitTimeWeight") or (key == "maxQueueLengthWeight"):
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
    print("Received junction data:", junctionData)  # Add this line for debugging

    if not junctionData:
        print("Error: Invalid data received.")  # Debugging
        return jsonify({"Error": "Invalid Data"}), 400

    junctionInformation = []


    for key, value in junctionData.items():
        if key == "junctionName":
            junctionInformation.append(value)
        elif key == "pedestrianCrossingAdded":
            junctionInformation.append(value.lower() == "yes")
        elif key in ["pedestrianCrossingDuration", "pedestrianCrossingRequests"] and value == "":
            junctionInformation.append(0)
        else:
            junctionInformation.append(int(value))

    # Insert into the database
    insertJunctionConfigurationsData(*junctionInformation)

    # Once junction is added, it is time to start simulating it

    return getAllJunctions()



# Help page
@app.route("/helpPage", methods=["POST", "GET"])
def helpPage():
    return render_template("helpPage.html")

# Ensures framework works
if __name__ == "__main__":
    app.run(debug=True)