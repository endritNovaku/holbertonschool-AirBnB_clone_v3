#!/usr/bin/python3
""" import app_views and create route to status """
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', method=['GET'], strict_slashes=False)
def get_status():
    """ return the status rout in json form """
    return jsonify({'status': 'OK'})
