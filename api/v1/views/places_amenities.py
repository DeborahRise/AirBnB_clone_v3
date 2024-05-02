#!/usr/bin/python3
"""  a new view for the link between Place objects and Amenity objects
that handles all default RESTFul API actions"""

from api.v1.views import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity
from flask import jsonify, abort

@app_views.route("places/<place_id>/amenities", strict_slashes=False, methods=["GET"])
def get_amenitiesOfPlace(place_id):
    place_obj = storage.get(Place, place_id)
    if not place_obj:
        abort(404)