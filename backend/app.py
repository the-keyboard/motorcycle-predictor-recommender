from flask import Flask, request, jsonify
import pandas as pd
import os
from flask_cors import CORS

# Import your ML models
from ml_models.recommender import ContentBasedRecommender
from ml_models.predictor import preprocess_data, build_model

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow CORS for frontend-backend connection

# Dynamically get file path
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, 'working_db_fin.csv')

# Load the dataset
bike_data = pd.read_csv(file_path)

# Initialize models
content_recommender = ContentBasedRecommender(bike_data)
preprocessor, _ = preprocess_data(bike_data)
price_model = build_model(bike_data, preprocessor)

# Home route
@app.route('/')
def home():
    return jsonify({'message': 'Welcome to the Bike Recommender API!'})

# Recommendation endpoint
@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        user_preferences = request.get_json()
        recommendations = content_recommender.predict(user_preferences)
        return jsonify(recommendations.to_dict(orient='records'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Price prediction endpoint
@app.route('/predict-price', methods=['POST'])
def predict_price():
    try:
        user_preferences = request.get_json()
        input_data = pd.DataFrame([user_preferences])
        predicted_price = price_model.predict(input_data)[0]
        return jsonify({'predicted_price': predicted_price})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Run server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
