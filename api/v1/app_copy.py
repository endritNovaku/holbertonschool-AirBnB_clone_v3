#!/usr/bin/python3
"""
Module starting the API
"""
from api.v1.views import app_views
from flask import Flask
from models import storage
from os import environ

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(self):
    """Clossing session method"""
    storage.close()

if __name__ == "__main__":
    env_host = environ.get('HBNB_API_HOST', deafault='0.0.0.0')
    env_port = environ.get('HBNB_API_PORT', default=5000)
    app.run(host=env_host, port=env_port, threaded=True)
