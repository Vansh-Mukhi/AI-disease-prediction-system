import os
import joblib
import numpy as np
from flask import Flask, request, jsonify

app = Flask(__name__)

MODELS_DIR = os.path.join(os.path.dirname(__file__), 'models')

# Global dictionary to hold models
models = {}

def load_models():
    """Load all models into memory"""
    disease_types = ['diabetes', 'heart', 'parkinsons', 'liver', 'kidney']
    for disease in disease_types:
        model_path = os.path.join(MODELS_DIR, f'{disease}_model.pkl')
        if os.path.exists(model_path):
            models[disease] = joblib.load(model_path)
            print(f"Loaded {disease} model.")
        else:
            print(f"Warning: {disease} model not found at {model_path}")

# Load models at startup
load_models()

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "models_loaded": list(models.keys())})

@app.route('/predict/<disease>', methods=['POST'])
def predict(disease):
    if disease not in models:
        return jsonify({"error": f"Model for {disease} not available"}), 404
    
    try:
        data = request.json
        if not data or 'features' not in data:
            return jsonify({"error": "Invalid input format. Expected JSON with 'features' list."}), 400
        
        # Convert input features to numpy array
        features = np.array(data['features']).reshape(1, -1)
        
        # Get the appropriate model
        model = models[disease]
        
        # Predict class and probabilities
        prediction = model.predict(features)[0]
        probabilities = model.predict_proba(features)[0]
        
        # The probability of the positive class (assuming index 1 is positive)
        confidence = float(probabilities[1]) if len(probabilities) > 1 else float(probabilities[0])
        
        return jsonify({
            "disease": disease,
            "prediction": int(prediction),
            "confidence_score": confidence,
            "probabilities": probabilities.tolist()
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
