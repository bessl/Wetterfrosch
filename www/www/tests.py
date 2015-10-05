import unittest
import transaction
import datetime

from pyramid import testing

from .models import DBSession


class TestMyViewSuccessCondition(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        from sqlalchemy import create_engine
        engine = create_engine('sqlite://')
        from .models import (
            Base,
            Measurement,
            )
        DBSession.configure(bind=engine)
        Base.metadata.create_all(engine)
        with transaction.manager:
            model = Measurement(id=1, at=datetime.datetime.now(), temperature=23, humidity=40)
            DBSession.add(model)

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def test_passing_view(self):
        from .views import start
        request = testing.DummyRequest()
        info = start(request)
        #FIXME: testing
        #self.assertEqual(info['one'].name, 'one')


class TestMyViewFailureCondition(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        from sqlalchemy import create_engine
        engine = create_engine('sqlite://')
        from .models import (
            Base,
            Measurement,
            )
        DBSession.configure(bind=engine)

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def test_failing_view(self):
        from .views import start
        request = testing.DummyRequest()
        info = start(request)
        self.assertEqual(info.status_int, 500)