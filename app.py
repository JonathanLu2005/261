from flask import Flask, render_template, request, jsonify, redirect, url_for
from database.database import (
    insertModelTrafficFlowData,
    retrieveAllModelNames,
    insertJunctionConfigurationsData,
    retrieveAllModelJunctions
)

# Create web app
app = Flask(__name__)

# Model page
@app.route("/", methods=["GET"])
def modelPage():
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

    print(modelData)
    
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
    model_id = request.args.get("modelId")
    model_name = request.args.get("modelName")

    # Print the model details for debugging
    print(f"Received model_id: {model_id}, model_name: {model_name}")

    if not model_id:
        return redirect(url_for("modelPage"))

    # For now, just print a static response for junctions to simulate the data being returned.
    # Normally, this would be fetched from the database.
    junctions = [
        {"id": 1, "name": "Junction 1", "lanes": 3},
        {"id": 2, "name": "Junction 2", "lanes": 2},
        {"id": 3, "name": "Junction 3", "lanes": 4},
    ]
    
    print(f"Fetched junctions: {junctions}")  # Print junctions for debugging

    return render_template("junctionPage.html", model_id=model_id, model_name=model_name, junctions=junctions)


# Add junction with model ID
@app.route("/addJunction", methods=["POST"])
def addJunction():
    # Expecting JSON data from the frontend (for now, this is the junction data received)
    junctionData = request.json

    # Print the received junction data to verify it's coming through correctly
    print(f"Received junction data: {junctionData}")

    if not junctionData or "modelId" not in junctionData:
        return jsonify({"Error": "Invalid Data"}), 400

    # Here we would normally insert into the database, but for now, we simply print it.
    print(f"Junction data (without DB insert): {junctionData}")

    # Send a success response
    return jsonify({"Success": True})

# Help page
@app.route("/helpPage", methods=["POST", "GET"])
def helpPage():
    return render_template("helpPage.html")

# Ensures framework works
if __name__ == "__main__":
    app.run(debug=True)