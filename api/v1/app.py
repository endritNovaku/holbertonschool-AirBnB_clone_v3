#!/usr/bin/python3
"""
Module starting the API
"""
from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from models import storage
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})

env_host = getenv('HBNB_API_HOST', '0.0.0.0')
env_port = getenv('HBNB_API_PORT', 5000)

app.register_blueprint(app_views)


@app.teardown_appcontext
def close(self):
    """Clossing session method"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """
    Error handler for 404 errors that returns a JSON-formatted
    404 status code response
    """
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    """
    Main flask app
    """
    app.run(host=env_host, port=env_port, threaded=True)
