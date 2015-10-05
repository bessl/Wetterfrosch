import unittest
import transaction
import datetime

from pyramid import testing
from .models import DBSession, Measurement
from www.views import add

def _initTestingDB():
    from sqlalchemy import create_engine
    from www.models import (
        DBSession,
        Measurement,
        Base
        )
    engine = create_engine('sqlite://')
    Base.metadata.create_all(engine)
    DBSession.configure(bind=engine)
    with transaction.manager:
        model = Measurement(id=1, at=datetime.datetime.now(), temperature=13, humidity=40)
        DBSession.add(model)
    return DBSession


class AddMeasurementDataTests(unittest.TestCase):
    def setUp(self):
        self.session = _initTestingDB()
        self.config = testing.setUp()
        self.config.add_route('add', 'add/')

    def tearDown(self):
        self.session.remove()
        testing.tearDown()

    def test_only_post_request_allowed(self):
        request = testing.DummyRequest(params={'t': 12, 'h': 34}, post=None)
        response = add(request)
        self.assertEqual(response.status_code, 500)

    def test_only_full_data_request_allowed(self):
        request = testing.DummyRequest(params={'t': 12}, post=True)
        response = add(request)
        self.assertEqual(response.status_code, 500)

        request2 = testing.DummyRequest(params={'h': 99}, post=True)
        response2 = add(request2)
        self.assertEqual(response2.status_code, 500)

    def test_save_request(self):
        request = testing.DummyRequest(params={'t': 23, 'h': 24}, post=True)
        response = add(request)
        self.assertEqual(response.status_code, 200)

        m = self.session.query(Measurement).filter_by(temperature=23).one()
        self.assertEqual(m.humidity, 24)

        count_current = len(self.session.query(Measurement).all())
        self.assertEqual(count_current, 2)

        self.assertEqual(m.humidity, 24)
        self.assertEqual(m.temperature, 23)
        self.assertEqual(m.at.strftime("%d%m%Y%H"), datetime.datetime.now().strftime("%d%m%Y%H"))
