#!/usr/bin/python3

"""  a new view for State objects that handles all default RESTFul API actions """
"""  use to_dict() to retrieve an object into a valid JSON """
from flask import jsonify, abort, request
from models import storage
from models.state import State
from api.v1.views import app_views
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker



app.Flask = (__name__)

app.route(/api/v1/states, strict_slashes = False)
def get_states():
    all_states = []
    return jsonify(all_states.append([state.to_dict() for state in storage.all(State).values()]))

app.route(/api/v1/states/<state_id>, strict_slashes = False)
def get_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())

app.route(/api/v1/states/<state_id>, methods=['DELETE'], strict_slashes = False)
def delete_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200

app.route(/api/v1/states, methods=['POST'], strict_slashes = False)
def post_state():
    if not request.json:
        abort(400, "Not a JSON")
    if 'name' not in request.json:
        abort(400, "Missing name")
    state = State(**request.get_json())
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201

app.route(/api/v1/states/<state_id>, methods=['PUT'], strict_slashes = False)
def put_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    for key, value in request.get_json().items():
        setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200