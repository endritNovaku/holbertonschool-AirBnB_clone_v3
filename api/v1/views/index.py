#!/usr/bin/python3
""" import app_views and create route to status """
from api.v1.views import app_views
from flask import jsonify, request


@app_views.route('/status', methods=['GET'])
def get_status():
    """ return the status rout in json form """
    if request.method == 'GET':
        response = {"status": 'OK'}
        return jsonify(response)
