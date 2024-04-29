#!/usr/bin/python3
""" new view for User object that handles all default RESTFul API actions """

from api.v1.views import app_views
import models
from models.user import User
from models import storage
from flask import jsonify, request, abort


@app_views.route("/users", strict_slashes=False, methods=["GET"])
def get_users():
    """ retrieves  LIST of all users """
    listofusers = []
    all_users = storage.all(User).values()
    for all_user in all_users:
        listofusers.append(all_user.to_dict())
    return jsonify(listofusers)


@app_views.route("/users/<user_id>", strict_slashes=False, methods=["GET"])
def get_user(user_id):
    """ Gets a user object """
    user_obj = storage.get(User, user_id)
    if user_obj is None:
        abort(404)
    return jsonify(user_obj.to_dict())


@app_views.route("/users/<user_id>", strict_slashes=False, methods=["DELETE"])
def delete_user(user_id):
    """ Deletes a user object"""
    user_obj = storage.get(User, user_id)
    if user_obj is None:
        abort(404)
    storage.delete(user_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", strict_slashes=False, methods=["POST"])
def create_user():
    """ Create Users"""
    user_obj = request.get_json(force=True, silent=True)
    if not user_obj:
        abort(400, "Not a JSON")
    if 'email' not in user_obj:
        abort(400, "Missing email")
    if 'password' not in user_obj:
        abort(400, "Missing password")
    user_data = User(**user_obj)
    user_data.save()
    return jsonify(user_data.to_dict()), 201


@app_views.route("/users/<user_id>", strict_slashes=False, methods=["PUT"])
def update_user(user_id):
    """ Updates a User object: PUT /api/v1/users/<user_id> """
    user_obj = storage.get(User, user_id)
    if not user_obj:
        abort(404)
    user_data = request.get_json(force=True, silent=True)
    if not user_data:
        abort(400, "Not a JSON")
    for key, value in user_data.items():
        if key not in ["id", "email", "created_at", "updated_at"]
        setattr(user_obj, key, value)
    user_obj.save()
    return jsonify(user_obj.to_dict()), 200
