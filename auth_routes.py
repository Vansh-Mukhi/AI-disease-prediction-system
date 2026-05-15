from flask import Blueprint, request, jsonify, current_app
from auth.jwt_handler import sign_jwt
import bcrypt
import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json
    if not data or not data.get('email') or not data.get('password') or not data.get('name'):
        return jsonify({'message': 'Missing required fields'}), 400

    db = current_app.db
    
    # Check if user exists
    if db.users.find_one({"email": data['email']}):
        return jsonify({'message': 'User already exists'}), 409

    # Hash password
    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

    user = {
        "name": data['name'],
        "email": data['email'],
        "password": hashed_password.decode('utf-8'),
        "created_at": datetime.datetime.utcnow()
    }

    result = db.users.insert_one(user)
    token = sign_jwt(str(result.inserted_id))

    return jsonify({
        'message': 'User created successfully',
        'token': token,
        'user': {
            'id': str(result.inserted_id),
            'name': user['name'],
            'email': user['email']
        }
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Missing required fields'}), 400

    db = current_app.db
    user = db.users.find_one({"email": data['email']})

    if not user:
        return jsonify({'message': 'Invalid email or password'}), 401

    if bcrypt.checkpw(data['password'].encode('utf-8'), user['password'].encode('utf-8')):
        token = sign_jwt(str(user['_id']))
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': {
                'id': str(user['_id']),
                'name': user['name'],
                'email': user['email']
            }
        }), 200

    return jsonify({'message': 'Invalid email or password'}), 401
