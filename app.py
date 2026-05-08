from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import joblib
import numpy as np
 
app = Flask(__name__)
 
# MongoDB Atlas Connection
try:
    client = MongoClient(
        "mongodb+srv://aadhict22_db_user:Test1234@flaskproject.dl3ev76.mongodb.net/?appName=FlaskProject"
    )
 
    # Test Connection
    client.admin.command('ping')
 
    db = client["tourismDB"]
    collection = db["predictions"]
 
    print("MongoDB connected successfully")
 
except Exception as e:
    print(f"MongoDB connection failed: {e}")
    client = None
    db = None
    collection = None
 
# Load ML Model
model = joblib.load("tourism_model.pkl")
 
# Error handlers to return JSON instead of HTML
@app.errorhandler(404)
def not_found_handler(e):
    return jsonify({"error": "Route not found"}), 404
 
@app.errorhandler(405)
def method_not_allowed_handler(e):
    return jsonify({"error": "Method not allowed"}), 405
 
@app.errorhandler(500)
def internal_error_handler(e):
    return jsonify({"error": "Internal server error"}), 500
 
# Home Page
@app.route('/')
def home():
    return render_template('index.html')
 
# Prediction Route
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        print(f"Received request data: {data}")
 
        if data is None:
            return jsonify({"error": "No JSON data received"}), 400
 
        tourists = int(data.get('tourists', 0))
        temperature = int(data.get('temperature', 0))
        holiday = int(data.get('holiday', 0))
        event = int(data.get('event', 0))
 
        print(f"Parsed values - tourists: {tourists}, temp: {temperature}, holiday: {holiday}, event: {event}")
 
        input_data = np.array([[tourists, temperature, holiday, event]])
        print(f"Input data shape: {input_data.shape}")
 
        prediction = model.predict(input_data)
        print(f"Prediction: {prediction}")
 
        revenue = round(float(prediction[0]), 2)
 
        print("Collection value:", collection)
 
        # Store prediction in MongoDB
        if collection is not None:
 
            try:
 
                prediction_data = {
                    "tourists": tourists,
                    "temperature": temperature,
                    "holiday": holiday,
                    "event": event,
                    "predicted_revenue": revenue
                }
 
                result = collection.insert_one(prediction_data)
 
                print("Prediction stored in MongoDB")
                print("Inserted ID:", result.inserted_id)
 
            except Exception as mongo_error:
                print("Mongo Insert Error:", mongo_error)
 
        print(f"Prediction successful: revenue = {revenue}")
 
        response_data = {
            "predicted_revenue": revenue
        }
 
        print(f"Sending response: {response_data}")
 
        return jsonify(response_data), 200
 
    except Exception as e:
        print(f"Prediction error: {str(e)}")
 
        import traceback
        traceback.print_exc()
 
        return jsonify({"error": str(e), "type": type(e).__name__}), 500
 
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
 