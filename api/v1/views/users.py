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
    if not all_users:
        abort(404)
    for all_user in all_users:
        listofusers.append(all_user.to_dict())
    return jsonify(listofusers)


@app_views.route("/users/<user_id>", strict_slashes=False, methods=["GET"])
def get_user(user_id):
    user_obj = storage.get(User, user_id)
    if user_obj is None:
        abort(404)
    return jsonify(user_obj.to_dict())