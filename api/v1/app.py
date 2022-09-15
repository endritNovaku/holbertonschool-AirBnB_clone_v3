#!/usr/bin/python3
"""
Module starting the API
"""
from api.v1.views import app_views
from flask import Flask
from models import storage
from os import getenv


app = Flask(__name__)

env_host = getenv('HBNB_API_HOST', '0.0.0.0')
env_port = getenv('HBNB_API_PORT', 5000)

app.register_blueprint(app_views)


@app.teardown_appcontext
def close(self):
    """Clossing session method"""
    storage.close()

if __name__ == "__main__":
    """
    Main flask app
    """
    app.run(host=env_host, port=env_port, threaded=True)
