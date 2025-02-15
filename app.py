from flask import Flask, render_template, request, jsonify
from database.database import fetchAllTables

# Create web app
app = Flask(__name__)

# Dummy database
models = []

# Model page
@app.route("/", methods=["GET"])
def modelPage():
    testingConnection = fetchAllTables()

    print(testingConnection)

    return render_template("modelPage.html")

# Add model to model page
@app.route('/addModel', methods=["POST"])
def addModel():
    modelData = request.json 

    if not modelData or 'name' not in modelData: 
        return jsonify({"Error": "Invalid Data"}), 400 
    
    for key, value in modelData.items():
        print(key)
        print(value)
    
    newModel = {
        "id": len(models) + 1,
        "name": modelData["name"],
    }

    

    models.append(newModel)
    return jsonify(newModel)

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