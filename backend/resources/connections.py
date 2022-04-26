from flask_restful import Resource
import requests
from webargs import fields
from webargs.flaskparser import use_kwargs



class Connections(Resource):

    @use_kwargs({
      "_from": fields.Str(required=True),
      "to": fields.Str(required=True),
      "date": fields.Str(required=True),
      "time": fields.Str(required=True)},
      location="query"
      )
    def get(self,_from, to, date, time):
        """
        Connection request
        ---
        description: "Returns all the stations."
        parameters:
          - in: query
            name: _from
            description: departure station
          - in: query
            name: to
            description: destination station
          - in: query
            name: date
            description: travel date
          - in: query
            name: time
            description: travel time


        responses:
          200:
            description: Accepted
          400:
            description: to not set
          404:
            description: Could not match 'query' with a station id in iRail
          500:
            description: Could not match get data

        """
        URI = 'https://api.irail.be//connections/?from={}&to={}&date={}&time={}&format=json&alerts=false&results=1'.format(_from,to,date,time)
        request = requests.get(URI)
        return request.json() , request.status_code
