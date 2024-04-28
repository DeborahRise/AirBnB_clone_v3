#!/usr/bin/python3

""" A new view for State objects that handles all default RESTFul API actions """
""" Use to_dict() to retrieve an object into a valid JSON """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State

@app_views.route('/api/v1/states', methods=['GET'], strict_slashes=False)
def get_states():
    all_states = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(all_states)

@app_views.route('/api/v1/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())

@app_views.route('/api/v1/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200

@app_views.route('/api/v1/states', methods=['POST'], strict_slashes=False)
def post_state():
    if not request.json:
        abort(400, "Not a JSON")
    if 'name' not in request.json:
        abort(400, "Missing name")
    data = request.get_json()
    state = State(name=data['name'])
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201

@app_views.route('/api/v1/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
