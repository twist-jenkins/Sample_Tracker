#!/bin/env python

import unittest
import json
import os
import logging
logging.basicConfig(level=logging.INFO)

os.environ["WEBSITE_ENV"] = "Unittest"
# NOTE: because of the FLASK_APP.config.from_object(os.environ['APP_SETTINGS'])
# directive in the api code, importing the flask app must happen AFTER
# the os.environ Config above.
from app import app
from app import db
from app import login_manager

from test_flask_app import AutomatedTestingUser, RootPlate


class TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        login_manager.anonymous_user = AutomatedTestingUser
        cls.client = app.test_client()
        assert "Unittest" in os.environ["WEBSITE_ENV"]
        assert '@' not in app.config['SQLALCHEMY_DATABASE_URI']
        assert 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']
        db.create_all()
        cls.root_plate_barcode = RootPlate().create_in_db("XFER_ROOT",
                                                          db.engine)

    @classmethod
    def tearDownClass(cls):
        # cls._connection.destroy()
        # os.unlink(FLASK_APP.config['DATABASE'])  # delete filesystem sqlite
        pass

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

    def test_aliquot_standard_template_bad_source(self):
        data = {"sampleTransferTypeId": 1,
                "sampleTransferTemplateId": 1,  # ??
                "sourcePlates": [self.root_plate_barcode + '_WALDO'],
                "destinationPlates": ["test_aliquot_01a"]}
        rv = self.client.post('/api/v1/track-sample-step',
                              data=json.dumps(data),
                              content_type='application/json')
        assert rv.status_code == 200
        result = json.loads(rv.data)
        assert result["success"] is False

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

    def DISABLED_test_small_adhoc_golden(self):
        data = {"sampleTransferTypeId":13,
                "sampleTransferTemplateId":14,
                "transferMap":[{"source_plate_barcode":"XFER_ROOT","source_well_name":"A2","destination_plate_barcode":"ssdest000000141jul17_G","destination_well_name":"A1","destination_plate_well_count":96},{"source_plate_barcode":"XFER_ROOT","source_well_name":"A3","destination_plate_barcode":"ssdest000000141jul17_G","destination_well_name":"A2","destination_plate_well_count":96},{"source_plate_barcode":"XFER_ROOT","source_well_name":"A4","destination_plate_barcode":"ssdest000000141jul17_G","destination_well_name":"B6","destination_plate_well_count":96},{"source_plate_barcode":"XFER_ROOT","source_well_name":"A5","destination_plate_barcode":"ssdest000000141jul17_G","destination_well_name":"A4","destination_plate_well_count":96},{"source_plate_barcode":"XFER_ROOT","source_well_name":"A6","destination_plate_barcode":"ssdest000000141jul17_384_G","destination_well_name":"L1","destination_plate_well_count":384},{"source_plate_barcode":"XFER_ROOT","source_well_name":"A8","destination_plate_barcode":"ssdest000000141jul17_384_G","destination_well_name":"L12","destination_plate_well_count":384}]
                }
        rv = self.client.post('/api/v1/track-sample-step',
                              data=json.dumps(data),
                              content_type='application/json')
        assert rv.status_code == 200
        result = json.loads(rv.data)
        assert result["success"] is True

if __name__ == '__main__':
    unittest.main()
