#!/usr/bin/python3
"""Module defining Amenities API endpoints"""

from flask import Flask, abort, request, jsonify
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenities():
    """'/amenities route to display all amenities"""
    objects = storage.all(Amenity)
    amenities = []
    for amenity in objects.values():
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route('/amenities/<string:amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity_by_id(amenity_id):
    """'/amenities/<amenity_id>' route to get Amenity by object id"""
    amenityObject = storage.get(Amenity, amenity_id)
    if amenityObject is None:
        abort(404)
    return jsonify(amenityObject.to_dict())


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def post_amenities():
    """A route that creates an amenity"""
    req_body = None
    try:
        req_body = request.get_json()
        if not req_body:
            raise TypeError("Invalid")
    except Exception:
        abort(400, {'Not a JSON'})
    if "name" not in req_body:
        abort(400, {'Missing name'})
    new_amenity_obj = Amenity(name=req_body['name'])
    storage.new(new_amenity_obj)
    storage.save()
    return jsonify(new_amenity_obj.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """This route updates amenity and returns a JSON response"""
    req_body = None
    try:
        req_body = request.get_json()
        if not req_body:
            raise TypeError("Invalid")
    except Exception:
        abort(400, {'Not a JSON'})
    amenityObject = storage.get(Amenity, amenity_id)
    if amenityObject is None:
        abort(404)
    ignoreKeys = ['id', 'created_at', 'updated_at']
    ret_obj = {}
    for key, val in req_body.items():
        if key not in ignoreKeys:
            setattr(amenityObject, key, val)
    storage.save()
    return jsonify(amenityObject.to_dict()), 200


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Route to delete an amenity"""
    amenityObject = storage.get(Amenity, amenity_id)
    if amenityObject is None:
        abort(404)
    storage.delete(amenityObject)
    storage.save()
    return jsonify({}), 200
