#!/usr/bin/python3
""" A place view to handle http request related places"""


from flask import Flask, jsonify, request
from models import storage
from models.place import Place
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places_by_city(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if city is None:
        return jsonify({'error': 'City not found'}), 404

    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places', methods=['GET'], strict_slashes=False)
def get_places():
    """Retrieves a list of all Place objects"""
    places = storage.all(Place).values()
    return jsonify([place.to_dict() for place in places])


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a specific Place object by ID"""
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object by ID"""
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({'error': 'Not found'}), 404
    storage.delete(place)
    storage.save()
    return jsonify({})


@app_views.route('/places', methods=['POST'], strict_slashes=False)
def create_place():
    """Creates a new Place object"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Not a JSON'}), 400

    if 'name' not in data:
        return jsonify({'error': 'Missing name'}), 400

    new_place = Place(**data)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object by ID"""
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({'error': 'Not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Not a JSON'}), 400

    for key, value in data.items():
        setattr(place, key, value)

    storage.save()
    return jsonify(place.to_dict())
