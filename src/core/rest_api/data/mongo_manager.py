from pymongo import MongoClient
from .models import UserDB
from src.core.rest_api.auth.security import pwd_context

# MongoDB client initialization
client = MongoClient("your_mongodb_uri")
db = client.your_db_name
users_collection = db.users


def create_user(user_data: dict) -> str:
    """
    Create a new user in the database.
    """
    user_data['hashed_password'] = pwd_context.hash(user_data['password'])
    del user_data['password']
    user = users_collection.insert_one(user_data)
    return str(user.inserted_id)


def get_user_by_username(username: str) -> UserDB:
    """
    Retrieve a user from the database by username.
    """
    user = users_collection.find_one({"username": username})
    if user:
        return UserDB(**user)


def get_user_data(data_collection, username: str):
    """
    Retrieve user data from a specified data collection by username.
    """
    user_data = data_collection.find_one({"username": username})
    return user_data
