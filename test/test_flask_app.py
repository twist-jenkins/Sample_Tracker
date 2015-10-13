#!/bin/env python

import unittest
import json
import os
import logging
logging.basicConfig(level=logging.INFO)

from flask_login import AnonymousUserMixin

os.environ["WEBSITE_ENV"] = "Unittest"
# NOTE: because of the FLASK_APP.config.from_object(os.environ['APP_SETTINGS'])
# directive in the api code, importing the flask app must happen AFTER
# the os.environ Config above.
from app import app
from app import db
from app import login_manager


class AutomatedTestingUser(AnonymousUserMixin):
    '''
    This is the object for representing an anonymous user.
    Here we add enough properties to work against existing API calls.
    '''
    @property
    def get_id(self):
        return "AutomatedTestingUser"

    @property
    def operator_id(self):
        return "TST"

    @property
    def first_and_last_name(self):
        return "Automated Testing"


class RootPlate(object):

    def create_in_db(self, barcode="TEST_ROOT", db_engine=None):
        """ Make a fake root plate "permanently" in the DB.
        TODO: use an API call instead of tightly coupling into
        app.routes. """
        from app.utils import scoped_session
        from app.models import create_destination_plate
        with scoped_session(db.engine) as db_session:
            operator = AutomatedTestingUser()
            destination_barcode = barcode
            storage_location_id = 'TEST_STORAGE_LOC'
            source_plate_type_id = 1
            plate = create_destination_plate(db_session, operator,
                                             destination_barcode,
                                             source_plate_type_id,
                                             storage_location_id)
        return destination_barcode


class TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        login_manager.anonymous_user = AutomatedTestingUser
        cls.client = app.test_client()
        assert "Unittest" in os.environ["WEBSITE_ENV"]
        assert '@' not in app.config['SQLALCHEMY_DATABASE_URI']
        assert 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']
        db.create_all()
        cls.root_plate_barcode = RootPlate().create_in_db("ROOT1", db.engine)

    @classmethod
    def tearDownClass(cls):
        # cls._connection.destroy()
        # os.unlink(FLASK_APP.config['DATABASE'])  # delete filesystem sqlite
        pass

    def test_get_404(self):
        rv = self.client.get('/testing_404_1982341982374')
        assert rv.status_code == 404

    def test_get_samples(self):
        rv = self.client.get('/samples')
        assert rv.status_code == 200
        assert rv.data == '[]'

    def test_get_plate_404(self):
        random_string = "2tp84ytcnp29cmty41p3984myt"
        rv = self.client.get('/api/v1/plate_barcodes/%s'
                             % random_string,
                             content_type='application/json')
        assert rv.status_code == 200  # TODO: this should be 404
        result = json.loads(rv.data)
        assert result["success"] is False

    def TODO_test_get_root_plate_golden(self):
        rv = self.client.get('/api/v1/plate_barcodes/%s'
                             % self.root_plate_barcode,
                             content_type='application/json')
        assert rv.status_code == 200
        result = json.loads(rv.data)
        print result
        assert result["success"] is True


if __name__ == '__main__':
    unittest.main()
