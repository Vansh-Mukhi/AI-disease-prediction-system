from flask import Blueprint, jsonify, current_app
from auth.jwt_handler import token_required
from bson.objectid import ObjectId

user_bp = Blueprint('user', __name__)

@user_bp.route('/profile', methods=['GET'])
@token_required
def get_profile(user_id):
    db = current_app.db
    user = db.users.find_one({"_id": ObjectId(user_id)}, {"password": 0})
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
        
    user['_id'] = str(user['_id'])
    return jsonify(user), 200

@user_bp.route('/history', methods=['GET'])
@token_required
def get_history(user_id):
    db = current_app.db
    
    # Get all history records for this user, sorted by newest first
    cursor = db.history.find({"user_id": user_id}).sort("timestamp", -1)
    
    history_list = []
    for record in cursor:
        record['_id'] = str(record['_id'])
        # Convert datetime to string
        if 'timestamp' in record:
            record['timestamp'] = record['timestamp'].isoformat()
        history_list.append(record)
        
    return jsonify({"history": history_list}), 200
