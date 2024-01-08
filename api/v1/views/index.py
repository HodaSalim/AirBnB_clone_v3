#!/usr/bin/python3
"""Flask application that handles status route declaration"""

from api.v1.views import app_views
from flask import jsonify
from models import storage

@app_views.route("/status", strict_slashes=False)
def view_status():
    """ View function that return a json message."""
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False)
def view_stats():
    """ Veiw function that retrieves the number of each object by type."""
    return jsonify({
        "amenities": models.storage.count(Amenity),
        "cities": models.storage.count(City),
        "places": models.storage.count(Place),
        "reviews": models.storage.count(Review),
        "states": models.storage.count(State),
        "users": models.storage.count(User)
    })
