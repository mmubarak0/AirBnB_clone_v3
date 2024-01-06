#!/usr/bin/python3
""" A state view to handle http request related state"""

from flask import Flask, jsonify, request
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves a list of all State objects"""
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Retrieves a specific State object by id"""
    state = storage.get(State, state_id)

    if state is None:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(state.to_dict())


de = 'DELETE'


@app_views.route('/states/<state_id>', methods=[de], strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object by ID"""
    state = storage.get(State, state_id)
    if state is None:
        return jsonify({'error': 'Not found'}), 404
    storage.delete(state)
    storage.save()
    return jsonify({})


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a new State object"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Not a JSON'}), 400

    if 'name' not in data:
        return jsonify({'error': 'Missing name'}), 400

    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates a State object by ID"""
    state = storage.get(State, state_id)
    if state is None:
        return jsonify({'error': 'Not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Not a JSON'}), 400

    for key, value in data.items():
        setattr(state, key, value)

    storage.save()
    return jsonify(state.to_dict())
