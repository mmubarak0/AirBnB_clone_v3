#!/usr/bin/python3
"""User view."""

from api.v1.views import app_views
from flask import jsonify, request
from models.engine.db_storage import classes
import models
from models.user import User


@app_views.route('/users', methods=['GET'])
def list_of_Users():
    """List all users."""
    users = [user.to_dict() for user in models.storage.all(User).values()]
    if users:
        return jsonify(users)
    return jsonify([]), 404


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    """Get User by id route."""
    user = models.storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    return jsonify({"error": "Not found"}), 404


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user_by_id(user_id):
    """Delete User by id route."""
    user = models.storage.get(User, user_id)
    if user:
        models.storage.delete(user)
        models.storage.save()
        return jsonify({}), 200
    return jsonify({"error": "Not found"}), 404


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Create User object route."""
    user_dict = {}
    try:
        user_dict = request.get_json()
    except Exception:
        pass
    if type(user_dict) is dict:
        if "email" in user_dict:
            if "password" in user_dict:
                user = User(**user_dict)
                user.save()
                return jsonify(user.to_dict()), 201
            return jsonify({"error": "Missing password"}), 400
        return jsonify({"error": "Missing email"}), 400
    return jsonify({"error": "Not a JSON"}), 400


@app_views.route('/users/<user_id>', methods=['PUT'])
def alter_user_by_id(user_id):
    """Alter User by id route."""
    user = models.storage.get(User, user_id)
    if user:
        try:
            data = request.get_json()
            dont_touch = ["id", "email", "created_at", "updated_at"]
            filtered_data = {
                key: data[key] for key in list(
                    filter(
                        lambda key: key not in dont_touch, data
                    )
                )
            }
            if type(data) is dict:
                for key, value in filtered_data.items():
                    setattr(user, key, value)
                user.save()
                return jsonify(user.to_dict()), 200
            return jsonify({"error": "Not a JSON"}), 400
        except Exception:
            return jsonify({"error": "Not a JSON"}), 400
    return jsonify({"error": "Not found"}), 404
