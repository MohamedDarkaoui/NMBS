from flask_restful import Resource
import requests
from webargs import fields
from webargs.flaskparser import use_kwargs
from flask import jsonify



class Here(Resource):

    @use_kwargs({
      "lat1": fields.Str(required=True),
      "long1": fields.Str(required=True),
      "lat2": fields.Str(required=True),
      "long2": fields.Str(required=True),
      "depTime": fields.Str(required=True)},

      location="query"
      )
    def get(self,lat1, long1, lat2, long2, depTime):
        """
        Connection request
        ---
        description: "Returns car."
        parameters:
          - in: query
            name: lat1
            description: origin latitude
          - in: query
            name: long1
            description: origin longitude
          - in: query
            name: lat2
            description: destination latitude
          - in: query
            name: long2
            description: destination longitude
          - in: query
            name: depTime
            description: departure time


        responses:
          200:
            description: Accepted
          400:
            description: Malformed request
          401:
            description: Unauthorized
          403:
            description: Not allowed
          500:
            description: Internal server error
        """
        api_key = 'FAjTH2tnUxc3JMoyPu_S1Z_h2teVvUPn5ePM1E3h1SI'
        URI = 'https://router.hereapi.com/v8/routes?transportMode=car&origin={},{}&destination={},{}&departureTime={}&return=summary&apikey={}'.format(lat1,long1,lat2,long2,depTime,api_key)

        req = requests.get(URI)

        return req.json(), req.status_code
