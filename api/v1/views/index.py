#!/usr/bin/python3
""" import app_views and create route to status """
from api.v1.views import app_views
from flask import jsonify, request
from models import storage


@app_views.route('/status', methods=['GET'])
def get_status():
    """ return the status rout in json form """
    if request.method == 'GET':
        response = {"status": 'OK'}
        return jsonify(response)


@app_views.route('/stats', methods=['GET'])
def stats():
    """Retrieve the number of each objects by type"""
    if request.method == 'GET':
        response = {
                "amenities": storage.count('Amenity'),
                "cities": storage.count('City'),
                "places": storage.count('Place'),
                "reviews": storage.count('Review'),
                "states": storage.count('State'),
                "users": storage.count('User')
                }
        return jsonify(response)
