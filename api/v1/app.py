#!/usr/bin/python3
"""API modules needed"""
from models import storage
from api.v1.views import app_views
from flask import Flask
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(self):
    """Method to handle teardown appcontext"""
    storage.close()


if __name__ == '__main__':
    env_host = getenv('HBNB_API_HOST')
    env_port = getenv('HBNB_API_PORT')
    app.run(host=env_host, port=env_port, threaded=True)
