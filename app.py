import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from database.mongo import init_db
from routes.auth_routes import auth_bp
from routes.predict_routes import predict_bp
from routes.user_routes import user_bp

def create_app():
    app = Flask(__name__)
    
    # Enable CORS for frontend domain
    CORS(app)
    
    # Initialize MongoDB
    init_db(app)

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(predict_bp, url_prefix='/api/predict')
    app.register_blueprint(user_bp, url_prefix='/api/user')

    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({"status": "healthy", "service": "backend api"})

    # Error handling
    @app.errorhandler(404)
    def not_found(e):
        return jsonify(error=str(e)), 404

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify(error=str(e)), 500

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
