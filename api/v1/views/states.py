#!/usr/bin/python3
""" State objects that handles RESTFul API module"""

from flask import Flask, abort, request, jsonify
from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """'/status' route to display state objects as JSON response"""
    objects = storage.all(State)
    lista = []
    for state in objects.values():
        lista.append(state.to_dict())
    return jsonify(lista)


@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state_by_id(state_id):
    """'/states/<state_id>' route to updates a State object id"""
    stateObject = storage.get(State, state_id)
    if stateObject is None:
        abort(404)
    return jsonify(stateObject.to_dict())


@app_views.route('/states', methods=['POST'],
                 strict_slashes=False)
def post_states():
    """A route that creates a state"""
    req_body = None
    try:
        req_body = request.get_json()
        if not req_body:
            raise TypeError("Invalid")
    except Exception:
        abort(400, {'Not a JSON'})
    if "name" not in req_body:
        abort(400, {'Missing name'})
    new_state_obj = State(name=req_body['name'])
    storage.new(new_state_obj)
    storage.save()
    return jsonify(new_state_obj.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def put_state(state_id):
    """This route updates state as JSON response"""
    req_body = None
    try:
        req_body = request.get_json()
        if not req_body:
            raise TypeError("Invalid")
    except Exception:
        abort(400, {'Not a JSON'})
    stateObject = storage.get(State, state_id)
    if stateObject is None:
        abort(404)
    ignoreKeys = ['id', 'created_at', 'updated_at']
    ret_obj = {}
    for key, val in req_body.items():
        if key not in ignoreKeys:
            setattr(stateObject, key, val)
    storage.save()
    return jsonify(stateObject.to_dict()), 200


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Route to delete a state"""
    stateObject = storage.get(State, state_id)
    if stateObject is None:
        abort(404)
    storage.delete(stateObject)
    storage.save()
    return jsonify({}), 200
