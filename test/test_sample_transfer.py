#!/bin/env python

import unittest
import json
import os
import logging
logging.basicConfig(level=logging.INFO)

os.environ["WEBSITE_ENV"] = "Local"

# NOTE: because of the FLASK_APP.config.from_object(os.environ['APP_SETTINGS'])
# directive in the api code, importing the flask app must happen AFTER
# the os.environ Config above.
from app import app
from app import db
from app import login_manager

from test_flask_app import AutomatedTestingUser, RootPlate, rnd_bc

class TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        login_manager.anonymous_user = AutomatedTestingUser
        cls.client = app.test_client()
        # assert "Unittest" in os.environ["WEBSITE_ENV"]
        assert 'localhost' in app.config['SQLALCHEMY_DATABASE_URI']
        assert 'postgres' in app.config['SQLALCHEMY_DATABASE_URI']
        db.create_all()
        cls.root_plate_barcode = 'SRN 000577 SM-30'  # qtray
        #cls.root_plate_barcode = RootPlate().create_in_db("XFER_ROOT",
        #                                                  db.engine)

    @classmethod
    def tearDownClass(cls):
        # cls._connection.destroy()
        # os.unlink(FLASK_APP.config['DATABASE'])  # delete filesystem sqlite
        pass

    def DISABLED_test_aliquot_standard_template_golden(self):
        data = {"sampleTransferTypeId": 1,
                "sampleTransferTemplateId": 2,  # ??
                "sourcePlates": [self.root_plate_barcode],
                "destinationPlates": [rnd_bc()]}
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
                "destinationPlates": [rnd_bc()]}
        rv = self.client.post('/api/v1/track-sample-step',
                              data=json.dumps(data),
                              content_type='application/json')
        assert rv.status_code == 404
        result = json.loads(rv.data)
        assert result["success"] is False

    def FUTURE_test_aliquot_user_defined_template_golden(self):
        data = {"sampleTransferTypeId": 1,
                "sampleTransferTemplate": {"foo": 3},  # ??
                "sourcePlates": [self.root_plate_barcode],
                "destinationPlates": [rnd_bc()]}
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
                "destinationPlates": [rnd_bc(), rnd_bc(), rnd_bc(), rnd_bc()]}
        rv = self.client.post('/api/v1/track-sample-step',
                              data=json.dumps(data),
                              content_type='application/json')
        assert rv.status_code == 200
        result = json.loads(rv.data)
        assert result["success"] is True

    def test_1_to_4_to_1_golden(self):
        intermediate_plates = [rnd_bc(), rnd_bc(), rnd_bc(), rnd_bc()]
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
                "destinationPlates": [rnd_bc()]}
        rv = self.client.post('/api/v1/track-sample-step',
                              data=json.dumps(data),
                              content_type='application/json')
        assert rv.status_code == 200
        result = json.loads(rv.data)
        assert result["success"] is True

    def DISABLED_test_small_adhoc_golden(self):
        bc = rnd_bc()
        bc2 = rnd_bc()
        transfer_map = [{
            "source_plate_barcode": self.root_plate_barcode,
            "source_well_name": src_well,
            "destination_plate_barcode": dest_plate,
            "destination_well_name": dest_well,
            "destination_plate_well_count": dest_well_count
        } for (src_well, dest_plate, dest_well, dest_well_count) in [
            ('A2', bc, 'A1', 96),
            ('A3', bc, 'A2', 96),
            ('A4', bc, 'B6', 96),
            ('A5', bc, 'A4', 96),
            ('A6', bc2, 'L1', 384),
            ('A8', bc2, 'L12', 384),
        ]]
        data = {"sampleTransferTypeId": 13,
                "sampleTransferTemplateId": 14,
                "transferMap": transfer_map
                }
        rv = self.client.post('/api/v1/track-sample-step',
                              data=json.dumps(data),
                              content_type='application/json')
        assert rv.status_code == 200, rv.data
        result = json.loads(rv.data)
        assert result["success"] is True

    def test_small_qpix_to_96_golden(self):
        rnd = rnd_bc()
        dest_plate_1_barcode = rnd + '_1'
        dest_plate_2_barcode = rnd + '_2'
        transfer_map = [{
            "source_plate_barcode": self.root_plate_barcode,
            "source_well_name": src_well,
            "destination_plate_barcode": dest_plate,
            "destination_well_name": dest_well,
            "destination_plate_well_count": dest_well_count
        } for (src_well, dest_plate, dest_well, dest_well_count) in [
            ('A1', dest_plate_1_barcode, 'A1', 96),
            ('A1', dest_plate_1_barcode, 'A2', 96),
            ('A2', dest_plate_1_barcode, 'B1', 96),
            ('B1', dest_plate_2_barcode, 'A1', 96),
            ('B1', dest_plate_2_barcode, 'A2', 96),
        ]]
        data = {"sampleTransferTypeId": 15,  # QPix To 96 plates
                "sampleTransferTemplateId": 21,
                "transferMap": transfer_map
                }
        rv = self.client.post('/api/v1/track-sample-step',
                              data=json.dumps(data),
                              content_type='application/json')
        assert rv.status_code == 200, rv.data
        result = json.loads(rv.data)
        assert result["success"] is True

        rv = self.client.get('/api/v1/plate-barcodes/%s'
                             % dest_plate_1_barcode,
                             content_type='application/json')
        assert rv.status_code == 200, rv.data
        result = json.loads(rv.data)
        print result
        assert result["success"] is True

    def test_small_ngs_prep_golden(self):
        rnd = rnd_bc()
        dest_plate_1_barcode = rnd + '_1'
        dest_plate_2_barcode = rnd + '_2'
        transfer_map = [{
            "source_plate_barcode": self.root_plate_barcode,
            "source_well_name": src_well,
            "destination_plate_barcode": dest_plate,
            "destination_well_name": dest_well,
            "destination_plate_well_count": dest_well_count
        } for (src_well, dest_plate, dest_well, dest_well_count) in [
            ('A1', dest_plate_1_barcode, 'A1', 96),
            ('A1', dest_plate_1_barcode, 'A2', 96),
            ('A2', dest_plate_1_barcode, 'B1', 96),
            ('B1', dest_plate_2_barcode, 'A1', 96),
            ('B1', dest_plate_2_barcode, 'A2', 96),
        ]]

        data = {"sampleTransferTypeId": 26,  # NGS Prep: Barcode Hitpicking
                "sampleTransferTemplateId": 21,
                "transferMap": transfer_map
                }
        rv = self.client.post('/api/v1/track-sample-step',
                              data=json.dumps(data),
                              content_type='application/json')
        assert rv.status_code == 200, rv.data
        result = json.loads(rv.data)
        assert result["success"] is True

        rv = self.client.get('/api/v1/plate-barcodes/%s'
                             % dest_plate_1_barcode,
                             content_type='application/json')
        assert rv.status_code == 200, rv.data
        result = json.loads(rv.data)
        print result
        assert result["success"] is True

if __name__ == '__main__':
    unittest.main()
