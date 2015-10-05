from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    Measurement,
    )


@view_config(route_name='home', renderer='templates/start.jinja2')
def start(request):
    try:
        one = DBSession.query(Measurement).first()
    except DBAPIError:
        return Response("Database Error", content_type='text/plain', status_int=500)
    return {'one': one, 'project': 'www'}


@view_config(route_name='add')
def add(request):
    # only post requests are allowed
    if request.method is not "POST":
        return Response("Request Error!", content_type='text/plain', status_int=500)

    # check for incoming data
    try:
        humidity = request.params['h']
        temperature = request.params['t']
    except(KeyError):
        return Response("Request Error 2!", content_type='text/plain', status_int=500)
    else:
        humidity = int(humidity)
        temperature = int(temperature)

    m = Measurement(temperature=temperature, humidity=humidity)
    DBSession.add(m)

    return Response('add done', status_int=200)


@view_config(route_name='current', renderer='json')
def current(request):
    m = DBSession.query(Measurement).order_by(Measurement.at.desc()).first()
    return {
        'humidity': m.humidity,
        'temperature': m.temperature,
        'at': str(m.at)
    }