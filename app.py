from flask import Flask, send_file, jsonify
import firebase_admin
from firebase_admin import credentials, db
import traceback

app = Flask(__name__)

# ---------------------------------------
# Firebase Admin SDK
# ---------------------------------------
try:
    cred = credentials.Certificate("serviceAccountKey.json")

    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://iots-2f517-default-rtdb.firebaseio.com/"
    })

    print("====================================")
    print("Firebase initialized successfully")
    print("====================================")

except Exception as e:
    print("====================================")
    print("Firebase initialization ERROR")
    print(e)
    print("====================================")
    traceback.print_exc()


# ---------------------------------------
# Get sensor data from Firebase
# ---------------------------------------
def get_sensor_data():

    try:
        ref = db.reference("/sensor")

        data = ref.get()

        print("Firebase data received:")
        print(data)

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

    except Exception as e:

        print("====================================")
        print("Firebase READ ERROR")
        print(e)
        print("====================================")

        traceback.print_exc()

        raise


# ---------------------------------------
# Home page
# ---------------------------------------
@app.route("/")
def index():
    return send_file("index.html")


# ---------------------------------------
# Sensor API
# ---------------------------------------
@app.route("/api/sensor")
def sensor():

    try:
        data = get_sensor_data()

        return jsonify(data)

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# ---------------------------------------
# Health check
# ---------------------------------------
@app.route("/health")
def health():

    return jsonify({
        "status": "Flask server running",
        "firebase": "connected"
    })


# ---------------------------------------
# Run Flask
# ---------------------------------------
if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
