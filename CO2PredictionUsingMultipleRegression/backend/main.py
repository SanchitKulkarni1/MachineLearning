from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib

app = Flask(__name__)
# Enable CORS to allow your React frontend to access the Flask server
CORS(app, resources={r"/*": {"origins": "*"}})

# Load the trained machine learning model (ensure the model is in the same directory or provide the correct path)
model = joblib.load('co2_emissions_model.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the JSON data sent from the frontend
        data = request.get_json()

        # Extract the values from the JSON payload
        engine_size = data.get("Engine Size")
        fuel_consumption = data.get("Fuel Consumption Combination")
        cylinders = data.get("Number of Cylinders")

        # Check if all required fields are provided
        if engine_size is None or fuel_consumption is None or cylinders is None:
            return jsonify({"error": "Missing required fields"}), 400

        # Make the prediction using the model
        prediction = model.predict([[engine_size, fuel_consumption, cylinders]])

        # Convert the prediction to a list (to make it JSON serializable)
        prediction_list = prediction.tolist()

        # Return the prediction as a JSON response
        return jsonify({"prediction": prediction_list[0]})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
