import os
from pymongo import MongoClient

def get_db():
    mongo_uri = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/medical_db')
    client = MongoClient(mongo_uri)
    db = client.get_default_database()
    return db

def init_db(app):
    app.db = get_db()
    # Create indexes for fast lookup
    app.db.users.create_index("email", unique=True)
