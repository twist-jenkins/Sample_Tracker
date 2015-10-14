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

    def create_in_db(self, db_engine=None):
        """ Make a fake root plate "permanently" in the DB.
        TODO: use an API call instead of tightly coupling into
        app.routes. """
        from app.utils import scoped_session
        from app.routes.angular import create_destination_plate
        with scoped_session(db.engine) as db_session:
            operator = AutomatedTestingUser()
            destination_barcode = 'TEST_ROOT'
            storage_location_id = 'TEST_STORAGE_LOC'
            source_plate_type_id = 1
            plate = create_destination_plate(db_session, operator,
                                             destination_barcode,
                                             source_plate_type_id,
                                             storage_location_id)
        return destination_barcode


class TestCase(unittest.TestCase):

    def setUp(self):
        login_manager.anonymous_user = AutomatedTestingUser
        self.client = app.test_client()
        assert "Unittest" in os.environ["WEBSITE_ENV"]
        assert '@' not in app.config['SQLALCHEMY_DATABASE_URI']
        assert 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']
        db.create_all()
        self.root_plate_barcode = RootPlate().create_in_db(db.engine)

    def tearDown(self):
        # os.unlink(FLASK_APP.config['DATABASE'])  # delete filesystem sqlite
        pass

    def test_get_404(self):
        rv = self.client.get('/testing_404_1982341982374')
        assert rv.status_code == 404

    def test_get_samples(self):
        rv = self.client.get('/samples')
        assert rv.status_code == 200
        assert rv.data == '[]'

    def xtest_get_plate_404(self):
        rv = self.client.get('/api/v1/plate_barcodes/%s'
                             % self.root_plate_barcode,
                             content_type='application/json')
        assert rv.status_code == 200
        result = json.loads(rv.data)
        assert result["success"] is False

    def xtest_get_root_plate_golden(self):
        rv = self.client.get('/api/v1/plate_barcodes/%s'
                             % self.root_plate_barcode,
                             content_type='application/json')
        assert rv.status_code == 200
        result = json.loads(rv.data)
        assert result["success"] is True

    def test_aliquot_standard_template_golden(self):
        data = {"sampleTransferTypeId": 1,
                "sampleTransferTemplateId": 1,  # ??
                "sourcePlates": [self.root_plate_barcode],
                "destinationPlates": ["test_aliquot_01a"]}
        rv = self.client.post('/api/v1/track-sample-step',
                              data=json.dumps(data),
                              content_type='application/json')
        assert rv.status_code == 200
        result = json.loads(rv.data)
        assert result["success"] is True

    def FUTURE_test_aliquot_user_defined_template_golden(self):
        data = {"sampleTransferTypeId": 1,
                "sampleTransferTemplate": {"foo": 3},  # ??
                "sourcePlates": [self.root_plate_barcode],
                "destinationPlates": ["test_aliquot_02a"]}
        rv = self.client.post('/api/v1/track-sample-step',
                              data=json.dumps(data),
                              content_type='application/json')
        assert rv.status_code == 200
        result = json.loads(rv.data)
        assert result["success"] is True

    def test_1_to_4_golden(self):
        data = {"sampleTransferTypeId": 11,
                "sampleTransferTemplateId": 13,
                "sourcePlates": [self.root_plate_barcode],
                "destinationPlates": ["tst14a", "tst14b", "tst14c", "tst14d"]}
        rv = self.client.post('/api/v1/track-sample-step',
                              data=json.dumps(data),
                              content_type='application/json')
        assert rv.status_code == 200
        result = json.loads(rv.data)
        assert result["success"] is True

    def test_1_to_4_to_1_golden(self):
        intermediate_plates = ["tst41a", "tst41b", "tst41c", "tst41d"]
        data = {"sampleTransferTypeId": 11,
                "sampleTransferTemplateId": 13,
                "sourcePlates": [self.root_plate_barcode],
                "destinationPlates": intermediate_plates}
        rv = self.client.post('/api/v1/track-sample-step',
                              data=json.dumps(data),
                              content_type='application/json')
        assert rv.status_code == 200

        data = {"sampleTransferTypeId": 17,
                "sampleTransferTemplateId": 18,
                "sourcePlates": intermediate_plates,
                "destinationPlates": ["tst41abcd"]}
        rv = self.client.post('/api/v1/track-sample-step',
                              data=json.dumps(data),
                              content_type='application/json')
        assert rv.status_code == 200
        result = json.loads(rv.data)
        assert result["success"] is True




if __name__ == '__main__':
    unittest.main()