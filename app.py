from flask import Flask, render_template, request, jsonify, redirect, url_for
from database.database import fetchAllTables, insertModelTrafficFlowData, retrieveAllModelNames

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
        # Frontend sends all data as a string, might need solve later but temporary fix here
        if key == "name":
            ModelInformation.append(value)
        elif (key == "maxWaitTimeWeight") or (key == "averageWaitTimeWeight") or (key == "maxQueueLengthWeight"):
            ModelInformation.append(float(value))
        else:
            ModelInformation.append(int(value))

    insertModelTrafficFlowData(*ModelInformation)

    # Return updated model list
    return getAllModels()

# Junction page
@app.route("/junctionPage", methods=["POST", "GET"])
def junctionPage():
    return render_template("junctionPage.html")

# Help page
@app.route("/helpPage", methods=["POST", "GET"])
def helpPage():
    return render_template("helpPage.html")

# Ensures framework works
if __name__ == "__main__":
    app.run(debug=True)