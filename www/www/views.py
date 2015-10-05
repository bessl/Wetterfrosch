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


