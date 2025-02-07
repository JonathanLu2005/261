from flask import Flask, render_template, request, jsonify

# Create web app
app = Flask(__name__)

# Create first route
@app.route("/", methods=["POST","GET"])
def home():
    return render_template("home.html")

# Ensures framework works
if __name__ == "__main__":
    app.run(debug=True)