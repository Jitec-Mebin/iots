from flask import Flask, render_template, jsonify
import firebase_admin
from firebase_admin import credentials, db

app = Flask(__name__)

# --------------------------------------------------
# Firebase initialization
# --------------------------------------------------

cred = credentials.Certificate("serviceAccountKey.json")

firebase_admin.initialize_app(cred, {
    "databaseURL": "https://iots-2f517-default-rtdb.firebaseio.com/"
})

# --------------------------------------------------
# Read sensor data
# --------------------------------------------------

def get_sensor_data():

    ref = db.reference("/sensor")
    data = ref.get()

    if data is None:
        return {
            "temperature": None,
            "humidity": None,
            "lastUpdate": None
        }

    return {
        "temperature": data.get("temperature"),
        "humidity": data.get("humidity"),
        "lastUpdate": data.get("lastUpdate")
    }


# --------------------------------------------------
# Dashboard
# --------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html")


# --------------------------------------------------
# API for live sensor data
# --------------------------------------------------

@app.route("/api/sensor")
def sensor():

    data = get_sensor_data()

    return jsonify(data)


# --------------------------------------------------
# Start Flask
# --------------------------------------------------

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )