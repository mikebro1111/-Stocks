from src.core.app import app
from src.core.app.auth import oauth
from flask import jsonify, request
from src.core.app.models.models import User, db


@app.route('/api/user', methods=['POST'])
def add_user():
    """
    Create a new user with the provided email address.
    """
    data = request.get_json()
    email = data.get('email')
    if not email:
        return jsonify({"error": "Email is required"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 400
    user = User(email=email)
    db.session.add(user)
    db.session.commit()
    return jsonify({"id": user.id, "email": user.email}), 201


@app.route('/api/users', methods=['GET'])
@oauth.require_oauth()
def get_users():
    """
    Retrieve a list of all users.
    """
    users = User.query.all()
    return jsonify([{"id": user.id, "email": user.email} for user in users])


@app.route('/api/user/<int:user_id>', methods=['PUT'])
@oauth.require_oauth()
def update_user(user_id):
    """
    Update the email address of an existing user.
    """
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    email = data.get('email')
    if email:
        user.email = email
    db.session.commit()
    return jsonify({"id": user.id, "email": user.email})


@app.route('/api/user/<int:user_id>', methods=['DELETE'])
@oauth.require_oauth()
def delete_user(user_id):
    """
    Delete an existing user.
    """
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"})


