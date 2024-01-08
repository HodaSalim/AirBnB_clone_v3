#!/usr/bin/python3
"""Module defining place_reviews API request methods"""

from flask import Flask, abort, request, jsonify
from api.v1.views import app_views
from models.place import Place
from models.review import Review
from models.user import User
from models import storage


@app_views.route('/places/<string:place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_place_reviews(place_id):
    """Route to fetch all reviews for a particular place"""
    place_obj = storage.get(Place, place_id)
    if not place_obj:
        abort(404)
    objects = storage.all(Review)
    place_reviews = []
    for review in objects.values():
        if review.place_id == place_id:
            place_reviews.append(review.to_dict())
    return jsonify(place_reviews)


@app_views.route('/reviews/<string:review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """Route to fetch a specific review"""
    reviewObject = storage.get(Review, review_id)
    if reviewObject is None:
        abort(404)
    return jsonify(reviewObject.to_dict())


@app_views.route('/places/<string:place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """A route that creates a review"""
    place_obj = storage.get(Place, place_id)
    if not place_obj:
        abort(404)
    req_body = None
    try:
        req_body = request.get_json()
        if not req_body:
            raise TypeError("Invalid")
    except Exception:
        abort(400, {'Not a JSON'})
    if "user_id" not in req_body:
        abort(400, {'Missing user_id'})
    user_obj = storage.get(User, req_body['user_id'])
    if not user_obj:
        abort(404)
    if "text" not in req_body:
        abort(400, {'Missing text'})
    new_review_obj = Review(
            text=req_body['text'],
            user_id=req_body['user_id'],
            place_id=place_id)
    storage.new(new_review_obj)
    storage.save()
    return jsonify(new_review_obj.to_dict()), 201


@app_views.route('/reviews/<string:review_id>', methods=['PUT'],
                 strict_slashes=False)
def put_review(review_id):
    """This route updates a review and returns a JSON response"""
    req_body = None
    try:
        req_body = request.get_json()
        if not req_body:
            raise TypeError("Invalid")
    except Exception:
        abort(400, {'Not a JSON'})
    reviewObject = storage.get(Review, review_id)
    if reviewObject is None:
        abort(404)
    ignoreKeys = ['id', 'created_at', 'user_id', 'place_id', 'updated_at']
    ret_obj = {}
    for key, val in req_body.items():
        if key not in ignoreKeys:
            setattr(reviewObject, key, val)
    storage.save()
    return jsonify(reviewObject.to_dict()), 200


@app_views.route('/reviews/<string:review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Route to delete a review"""
    reviewObject = storage.get(Review, review_id)
    if reviewObject is None:
        abort(404)
    storage.delete(reviewObject)
    storage.save()
    return jsonify({}), 200
