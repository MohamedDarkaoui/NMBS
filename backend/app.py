from flask import Flask
from flask_restful import Api

from backend.resources.station import Station
from backend.resources.connections import Connections
from backend.resources.here import Here
from flasgger import Swagger


def create_app():
    app = Flask(__name__)
    api = Api(app)
    swag = Swagger(app)

    api.add_resource(Station, '/api/stations')
    api.add_resource(Connections, '/api/connections')
    api.add_resource(Here, '/api/here')

    return app
