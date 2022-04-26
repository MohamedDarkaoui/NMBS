from flask_restful import Resource
import requests
from webargs import fields
from webargs.flaskparser import use_kwargs


class Station(Resource):
    def get_stations(self):
        URI = 'https://api.irail.be/stations/?format=json&lang=en'
        return requests.get(URI).json()['station']

    def get(self):
        """
        Connection request
        ---
        description: "Returns all the stations."

        responses:
          200:
            description: Accepted
        """
        return self.get_stations(), 200
