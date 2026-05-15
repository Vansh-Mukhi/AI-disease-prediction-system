import os
import requests
import datetime
from flask import Blueprint, request, jsonify, current_app
from auth.jwt_handler import token_required

predict_bp = Blueprint('predict', __name__)
ML_SERVICE_URL = os.environ.get('ML_SERVICE_URL', 'http://localhost:5001')

@predict_bp.route('/<disease>', methods=['POST'])
@token_required
def predict_disease(user_id, disease):
    valid_diseases = ['diabetes', 'heart', 'parkinsons', 'liver', 'kidney']
    
    if disease not in valid_diseases:
        return jsonify({'message': 'Invalid disease type'}), 400

    data = request.json
    if not data or 'features' not in data:
        return jsonify({'message': 'Missing features for prediction'}), 400

    try:
        # Call ML Service
        response = requests.post(f"{ML_SERVICE_URL}/predict/{disease}", json={"features": data['features']})
        
        if response.status_code != 200:
            return jsonify({'message': 'Error from ML service', 'details': response.json()}), response.status_code
            
        result = response.json()
        
        # Save prediction history to DB
        db = current_app.db
        history_record = {
            "user_id": user_id,
            "disease": disease,
            "features": data['features'],
            "prediction": result['prediction'],
            "confidence_score": result['confidence_score'],
            "timestamp": datetime.datetime.utcnow()
        }
        db.history.insert_one(history_record)

        return jsonify({
            'message': 'Prediction successful',
            'result': result
        }), 200

    except Exception as e:
        return jsonify({'message': 'Failed to connect to ML service', 'error': str(e)}), 500
