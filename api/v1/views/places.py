#!/usr/bin/python3
""" Module defining place API request methods"""

from flask import Flask, abort, request, jsonify
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User
from models import storage


@app_views.route('/cities/<string:city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_city_places(city_id):
    """Route to fetch all places for a particular city"""
    city_obj = storage.get(City, city_id)
    if not city_obj:
        abort(404)
    objects = storage.all(Place)
    city_places = []
    for place in objects.values():
        if place.city_id == city_id:
            city_places.append(place.to_dict())
    return jsonify(city_places)


@app_views.route('/places/<string:place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """Route to fetch a specific place"""
    placeObject = storage.get(Place, place_id)
    if placeObject is None:
        abort(404)
    return jsonify(placeObject.to_dict())


@app_views.route('/cities/<string:city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """A route that creates a place"""
    city_obj = storage.get(City, city_id)
    if not city_obj:
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
    if "name" not in req_body:
        abort(400, {'Missing name'})
    new_place_obj = Place(
            name=req_body['name'],
            user_id=req_body['user_id'],
            city_id=city_id)
    storage.new(new_place_obj)
    storage.save()
    return jsonify(new_place_obj.to_dict()), 201


@app_views.route('/places/<string:place_id>', methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id):
    """This route updates place and returns a JSON response"""
    req_body = None
    try:
        req_body = request.get_json()
        if not req_body:
            raise TypeError("Invalid")
    except Exception:
        abort(400, {'Not a JSON'})
    placeObject = storage.get(Place, place_id)
    if placeObject is None:
        abort(404)
    ignoreKeys = ['id', 'created_at', 'user_id', 'city_id', 'updated_at']
    ret_obj = {}
    for key, val in req_body.items():
        if key not in ignoreKeys:
            setattr(placeObject, key, val)
    storage.save()
    return jsonify(placeObject.to_dict()), 200


@app_views.route('/places/<string:place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Route to delete a place"""
    placeObject = storage.get(Place, place_id)
    if placeObject is None:
        abort(404)
    storage.delete(placeObject)
    storage.save()
    return jsonify({}), 200
