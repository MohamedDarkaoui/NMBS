from flask_restful import Resource
import requests
from webargs import fields
from webargs.flaskparser import use_kwargs



class Here(Resource):

    @use_kwargs({
      "lat1": fields.Str(required=True),
      "long1": fields.Str(required=True),
      "lat2": fields.Str(required=True),
      "long2": fields.Str(required=True)},
      location="query"
      )
    def get(self,lat1, long1, lat2, long2):
        """
        Connection request
        ---
        description: "Returns car."
        parameters:
          - in: query
            name: lat1
            description: origin x coordinate
          - in: query
            name: long1
            description: origin y coordinate
          - in: query
            name: lat2
            description: destination x coordinate
          - in: query
            name: long2
            description: destination y coordinate


        responses:
          200:
            description: Accepted
        """
        api_key = 'FAjTH2tnUxc3JMoyPu_S1Z_h2teVvUPn5ePM1E3h1SI'
        URI = 'https://router.hereapi.com/v8/routes?transportMode=car&origin={},{}&destination={},{}&return=summary&apikey={}'.format(lat1,long1,lat2,long2,api_key)

        req = requests.get(URI).json()

        durations = []

        for route in req['routes']:
            duration = 0
            for section in route['sections']:
                duration += section['summary']['duration']
            durations.append(duration)

        return min(durations), 200
