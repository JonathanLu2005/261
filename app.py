from flask import Flask, render_template, request, jsonify, redirect, url_for
from database.database import fetchAllTables, insertModelTrafficFlowData, retrieveAllModelNames

# Create web app
app = Flask(__name__)

# Model page
@app.route("/", methods=["GET"])
def modelPage():
    CurrentModels = []

    AllModels = retrieveAllModelNames()

    if AllModels == []:
        return render_template("modelPage.html")
    
    print(AllModels)

    for ModelID, ModelName in AllModels:
        Model = {
            "id": ModelID,
            "name": ModelName
        }
        CurrentModels.append(Model)

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

    insertModelTrafficFlowData(ModelInformation[0], ModelInformation[1],
                               ModelInformation[2], ModelInformation[3], ModelInformation[4],
                               ModelInformation[5], ModelInformation[6], ModelInformation[7],
                               ModelInformation[8], ModelInformation[9], ModelInformation[10],
                               ModelInformation[11], ModelInformation[12], ModelInformation[13],
                               ModelInformation[14], ModelInformation[15], ModelInformation[16],
                               ModelInformation[17], ModelInformation[18], ModelInformation[19])

    return redirect(url_for('modelPage'))

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