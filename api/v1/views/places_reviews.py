#!/usr/bin/python3
""" new view for Review object that handles all default RESTFul API actions """

from api.v1.views import app_views
from models import storage
from models.user import User
from models.place import Place
from models.review import Review
from flask import jsonify, abort, request


@app_views.route("/places/<place_id>/reviews", strict_slashes=False,
                 methods=["GET"])
def get_reviews(place_id):
    """ Retrieves the list of all Review objects of a Place: GET
    /api/v1/places/<place_id>/reviews """

    place_obj = storage.get(Place, place_id)
    if not place_obj:
        abort(404)
    reviews_list = []
    all_reviews = storage.all(Review).values()
    for r in all_reviews:
        if r.place_id == place_id:
            reviews_list.append(r.to_dict())
    return jsonify(reviews_list)


@app_views.route("/reviews/<review_id>", strict_slashes=False,
                 methods=["GET"])
def get_review(review_id):
    """ Retrieves a Review object. : GET /api/v1/reviews/<review_id> """
    review_obj = storage.get(Review, review_id)
    if not review_obj:
        abort(404)
    return jsonify(review_obj.to_dict())


@app_views.route("reviews/<review_id>", strict_slashes=False,
                 methods=["DELETE"])
def delete_review(review_id):
    """ Deletes a Review object: DELETE /api/v1/reviews/<review_id> """
    review_obj = storage.get(Review, review_id)
    if not review_obj:
        abort(404)
    storage.delete(review_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", strict_slashes=False,
                 methods=["POST"])
def create_review(place_id):
    """ Creates a Review: POST /api/v1/places/<place_id>/reviews """
    place_obj = storage.get(Place, place_id)
    if not place_obj:
        abort(404)
    review_data = request.get_json(force=True, silent=True)
    if not review_data:
        abort(400, "Not a JSON")
    if "user_id" not in review_data:
        abort(400, "Missing user_id")
    user_obj = storage.get(User, review_data.get("user_id"))
    if not user_obj:
        abort(404)
    if "text" not in review_data:
        abort(400, "Missing text")
    new_review = Review(place_id=place_id, **review_data)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", strict_slashes=False,
                 methods=["PUT"])
def update_review(review_id):
    """ Updates a Review object: PUT /api/v1/reviews/<review_id> """
    review_obj = storage.get(Review, review_id)
    if not review_obj:
        abort(404)
    review_data = request.get_json(force=True, silent=True)
    if not review_data:
        abort(400, "Not a JSON")
    for key, value in review_data.items():
        if key not in ["id", "user_id", "place_id",
                       "created_at", "updated_at"]:
            setattr(review_obj, key, value)
    review_obj.save()
    return jsonify(review_obj.to_dict()), 200
