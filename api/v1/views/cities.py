#!/usr/bin/python3
""" Module defining city API request methods"""

from flask import Flask, abort, request, jsonify
from api.v1.views import app_views
from models.state import State
from models.city import City
from models import storage


@app_views.route('/states/<string:state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_state_cities(state_id):
    """Route to fetch all cities for a particular state"""
    state_obj = storage.get(State, state_id)
    if not state_obj:
        abort(404)
    objects = storage.all(City)
    state_cities = []
    for city in objects.values():
        if city.state_id == state_id:
            state_cities.append(city.to_dict())
    return jsonify(state_cities)


@app_views.route('/cities/<string:city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """Route to fetch a specific city"""
    cityObject = storage.get(City, city_id)
    if cityObject is None:
        abort(404)
    return jsonify(cityObject.to_dict())


@app_views.route('/states/<string:state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """A route that creates a city"""
    state_obj = storage.get(State, state_id)
    if not state_obj:
        abort(404)
    req_body = None
    try:
        req_body = request.get_json()
        if not req_body:
            raise TypeError("Invalid")
    except Exception:
        abort(400, {'Not a JSON'})
    if "name" not in req_body:
        abort(400, {'Missing name'})
    new_city_obj = City(name=req_body['name'], state_id=state_id)
    storage.new(new_city_obj)
    storage.save()
    return jsonify(new_city_obj.to_dict()), 201


@app_views.route('/cities/<string:city_id>', methods=['PUT'],
                 strict_slashes=False)
def put_city(city_id):
    """This route updates state as JSON response"""
    req_body = None
    try:
        req_body = request.get_json()
        if not req_body:
            raise TypeError("Invalid")
    except Exception:
        abort(400, {'Not a JSON'})
    cityObject = storage.get(City, city_id)
    if cityObject is None:
        abort(404)
    ignoreKeys = ['id', 'created_at', 'state_id', 'updated_at']
    ret_obj = {}
    for key, val in req_body.items():
        if key not in ignoreKeys:
            setattr(cityObject, key, val)
    storage.save()
    return jsonify(cityObject.to_dict()), 200


@app_views.route('/cities/<string:city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Route to delete a city"""
    cityObject = storage.get(City, city_id)
    if cityObject is None:
        abort(404)
    storage.delete(cityObject)
    storage.save()
    return jsonify({}), 200
