from flask_restful import Resource
import requests

URI = 'https://api.irail.be/stations/?format=json&lang=en'


def get_stations():
    return requests.get(URI).json()['station']


def get_station_names():
    names = []
    for station in get_stations():
        names.append(station['name'])

    return names


class Station(Resource):

    def get(self):
        return get_station_names()
