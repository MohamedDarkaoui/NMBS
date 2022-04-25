from flask import Flask
from flask_restful import Api

from backend.resources.station import Station


def create_app():
    app = Flask(__name__)
    api = Api(app)

    api.add_resource(Station, '/api/stations')

    return app
