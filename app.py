from flask import Flask, render_template, request, jsonify

# Create web app
app = Flask(__name__)

# Model page
@app.route("/", methods=["POST","GET"])
def modelPage():
    return render_template("modelPage.html")

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