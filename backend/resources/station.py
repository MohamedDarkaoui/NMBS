from flask import jsonify
from flask_restful import Resource
import requests
from webargs import fields
from webargs.flaskparser import use_kwargs


class Station(Resource):
    def get_stations(self):
        URI = 'https://api.irail.be/stations/?format=json&lang=en'
        return requests.get(URI)

    def get(self):
        """
        Connection request
        ---
        description: "Returns all the stations."

        responses:
          200:
            description: Accepted
        """
        request = self.get_stations()
        return request.json(), request.status_code
