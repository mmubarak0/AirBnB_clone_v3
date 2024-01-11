#!/usr/bin/python3
"""Amenity view."""

from api.v1.views import app_views
from flask import jsonify, request
from models.engine.db_storage import classes
import models
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'])
def list_of_amenities():
    """List all amenities."""
    amenities = [
                    amenity.to_dict() for amenity in models.storage.all(
                        Amenity
                    ).values()
                ]
    if amenities:
        return jsonify(amenities)
    return jsonify([]), 404


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity_by_id(amenity_id):
    """Get Amenity by id route."""
    amenity = models.storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    return jsonify({"error": "Not found"}), 404


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity_by_id(amenity_id):
    """Delete Amenity by id route."""
    amenity = models.storage.get(Amenity, amenity_id)
    if amenity:
        models.storage.delete(amenity)
        models.storage.save()
        return jsonify({}), 200
    return jsonify({"error": "Not found"}), 404


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Create Amenity object route."""
    amenity_dict = {}
    try:
        amenity_dict = request.get_json()
    except Exception:
        pass
    if type(amenity_dict) is dict:
        if "name" in amenity_dict:
            amenity = Amenity(**amenity_dict)
            amenity.save()
            return jsonify(amenity.to_dict()), 201
        return jsonify({"error": "Missing name"}), 400
    return jsonify({"error": "Not a JSON"}), 400


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def alter_amenity_by_id(amenity_id):
    """Alter Amenity by id route."""
    amenity = models.storage.get(Amenity, amenity_id)
    if amenity:
        try:
            data = request.get_json()
            dont_touch = ["id", "created_at", "updated_at"]
            filtered_data = {
                key: data[key] for key in list(
                    filter(
                        lambda key: key not in dont_touch, data
                    )
                )
            }
            if type(data) is dict:
                for key, value in filtered_data.items():
                    setattr(amenity, key, value)
                amenity.save()
                return jsonify(amenity.to_dict()), 200
            return jsonify({"error": "Not a JSON"}), 400
        except Exception:
            return jsonify({"error": "Not a JSON"}), 400
    return jsonify({"error": "Not found"}), 404
