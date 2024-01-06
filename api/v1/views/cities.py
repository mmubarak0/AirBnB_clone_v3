#!/usr/bin/python3
"""City view."""

from api.v1.views import app_views
from flask import jsonify, request
from models.engine.db_storage import classes
import models
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def list_cities_from_state(state_id):
    """Cities from state route."""
    state = models.storage.get(State, state_id)
    if state:
        cities = [city.to_dict() for city in state.cities]
        if cities:
            return jsonify(cities)
    return jsonify({"error": "Not found"}), 404


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city_by_id(city_id):
    """City by id route."""
    city = models.storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    return jsonify({"error": "Not found"}), 404


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city_by_id(city_id):
    """Delete City by id route."""
    city = models.storage.get(City, city_id)
    if city:
        models.storage.delete(city)
        models.storage.save()
        return jsonify({}), 200
    return jsonify({"error": "Not found"}), 404


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """Create City in a state route."""
    state = models.storage.get(State, state_id)
    if state:
        city_dict = request.get_json()
        if type(city_dict) is dict:
            if "name" in city_dict:
                city = City(**city_dict)
                city.state_id = state_id
                city.save()
                return jsonify(city.to_dict()), 201
            return jsonify({"error": "Missing name"}), 400
        return jsonify({"error": "Not a JSON"}), 400
    return jsonify({"error": "Not found"}), 404


@app_views.route('/cities/<city_id>', methods=['PUT'])
def alter_city_by_id(city_id):
    """Alter City by id route."""
    city = models.storage.get(City, city_id)
    if city:
        data = request.get_json()
        dont_touch = ["id", "state_id", "created_at", "updated_at"]
        filtered_data = {
            key: data[key] for key in list(
                filter(
                    lambda key: key not in dont_touch, data
                )
            )
        }
        if type(data) is dict:
            for key, value in filtered_data.items():
                setattr(city, key, value)
            city.save()
            return jsonify(city.to_dict()), 200
        return jsonify({"error": "Not a JSON"}), 400
    return jsonify({"error": "Not found"}), 404
