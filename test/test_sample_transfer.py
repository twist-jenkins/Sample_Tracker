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

from test_flask_app import AutomatedTestingUser, rnd_bc
# from test_flask_app import RootPlate

class TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        login_manager.anonymous_user = AutomatedTestingUser
        cls.client = app.test_client()
        assert 'localhost' in app.config['SQLALCHEMY_DATABASE_URI']
        assert 'postgres' in app.config['SQLALCHEMY_DATABASE_URI']
        cls.root_plate_barcode = 'SRN 000577 SM-30'  # qtray

    @classmethod
    def tearDownClass(cls):
        # cls._connection.destroy()
        # os.unlink(FLASK_APP.config['DATABASE'])  # delete filesystem sqlite
        pass

    def DEPRECATED_test_aliquot_standard_template_golden(self):
        data = {"sampleTransferTypeId": 2,
                "sampleTransferTemplateId": 1,
                "sourcePlates": [self.root_plate_barcode],
                "destinationPlates": [rnd_bc(), ]}
        rv = self.client.post('/api/v1/track-sample-step',
                              data=json.dumps(data),
                              content_type='application/json')
        assert rv.status_code == 200
        result = json.loads(rv.data)
        assert result["success"] is True

    def DEPRECATED_test_aliquot_standard_template_bad_source(self):
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

    def DEPRECATED_test_1_to_4_golden(self):
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

    def DEPRECATED_test_1_to_4_to_1_golden(self):
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

    def test_small_adhoc_golden(self):
        bc = rnd_bc()
        bc2 = rnd_bc()
        transfer_map = [{
            "source_plate_barcode": self.root_plate_barcode,
            # "source_well_name": src_well_name,
            "source_well_number": src_well_num,
            "destination_plate_barcode": dest_plate,
            # "destination_well_name": dest_well_name,
            "destination_well_number": dest_well_num,
            "destination_plate_well_count": dest_well_count,
            "destination_plate_type": 'SPTT_0006',
            "source_sample_id": src_sample_id
        } for (src_well_name, src_well_num, src_sample_id,
               dest_plate, dest_well_name, dest_well_num, dest_well_count) in [
            ('A1', 1, 'GA_562a647b799305708a87985f', bc, 'A1', 1, 96),
            ('A2', 2, 'GA_562a647b799305708a87985d', bc, 'A2', 2, 96),
            ('B1', 7, 'GA_562a647b799305708a879867', bc, 'B6', 30, 96),
            ('B2', 8, 'GA_562a647b799305708a879865', bc, 'A4', 4, 96),
            ('C1', 13, 'GA_562a647b799305708a87981f', bc2, 'L1', 265, 384),
            ('C2', 14, 'GA_562a647b799305708a87981d', bc2, 'L12', 276, 384),
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

    def test_small_same_to_same_golden(self):

        # verify initial sample

        sample_1_id = 'GA_562a647b799305708a87985f'
        order_item_id = 'WOI_56bc154100bc15c389b79190'
        plate_well_number = 1
        rv = self.client.get('/api/v1/rest/sample/%s' % sample_1_id,
                             content_type='application/json')
        assert rv.status_code == 200, rv.data
        result = json.loads(rv.data)
        assert result["errors"] == []
        assert result["data"]["order_item_id"] == order_item_id

        # stamp a test plate

        plate_2_barcode = rnd_bc()

        same2same = [
            (1, sample_1_id, 1, 48),
            (2, 'GA_562a647b799305708a87985d', 2, 48),
            (7, 'GA_562a647b799305708a879867', 7, 48),
            (8, 'GA_562a647b799305708a879865', 8, 48),
            (13, 'GA_562a647b799305708a87981f', 13, 48),
            (14, 'GA_562a647b799305708a87981d', 14, 48),
        ]

        transfer_map = [{
            "source_plate_barcode": self.root_plate_barcode,
            "source_well_number": src_well_num,
            "destination_plate_barcode": plate_2_barcode,
            "destination_well_number": dest_well_num,
            "destination_plate_well_count": dest_well_count,
            "destination_plate_type": 'SPTT_0004',
            "source_sample_id": src_sample_id
        } for (src_well_num, src_sample_id,
               dest_well_num, dest_well_count) in same2same]
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

        rv = self.client.get('/api/v1/rest/plate/%s/well/1' % plate_2_barcode,
                              data=json.dumps(data),
                              content_type='application/json')
        assert rv.status_code == 200, rv.data
        result = json.loads(rv.data)
        assert result["errors"] == []
        assert result["data"]["parent_sample_id"] == sample_1_id
        assert result["data"]["plate_well_code"] == 300480001
        assert result["data"]["order_item_id"] == order_item_id


        # then same2same the result

        plate_3_barcode = rnd_bc()

        for op in transfer_map:
            op["source_plate_barcode"] = plate_2_barcode
            op["source_plate_barcode"] = plate_2_barcode

        data = {"sampleTransferTypeId": 62,  # "CHP Deprotection"
                "sampleTransferTemplateId": 2,  # Same - Same
                "transferMap": transfer_map
                }
        rv = self.client.post('/api/v1/track-sample-step',
                              data=json.dumps(data),
                              content_type='application/json')
        assert rv.status_code == 200, rv.data
        result = json.loads(rv.data)
        assert result["success"] is True

        # now verify the sample is intact

        rv = self.client.get('/api/v1/rest/sample/%s' % sample_1_id,
                             content_type='application/json')
        assert rv.status_code == 200, rv.data
        result = json.loads(rv.data)
        assert result["errors"] == []

    def xtest_small_same_to_same_to_same_golden(self):

        bc = rnd_bc()

        same2same = [
            (1, 'GA_562a647b799305708a87985f', bc, 1, 48),
            (2, 'GA_562a647b799305708a87985d', bc, 2, 48),
            (7, 'GA_562a647b799305708a879867', bc, 7, 48),
            (8, 'GA_562a647b799305708a879865', bc, 8, 48),
            (13, 'GA_562a647b799305708a87981f', bc, 13, 48),
            (14, 'GA_562a647b799305708a87981d', bc, 14, 48),
        ]

        # stamp a test plate
        transfer_map = [{
            "source_plate_barcode": self.root_plate_barcode,
            "source_well_number": src_well_num,
            "destination_plate_barcode": dest_plate,
            "destination_well_number": dest_well_num,
            "destination_plate_well_count": dest_well_count,
            "destination_plate_type": 'SPTT_0004',
            "source_sample_id": src_sample_id
        } for (src_well_num, src_sample_id,
               dest_plate, dest_well_num, dest_well_count) in same2same]
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

        # then same2same the result a few times

        for op in transfer_map:
            op["source_plate_barcode"] = bc

        data = {"sampleTransferTypeId": 62,  # "CHP Deprotection"
                "sampleTransferTemplateId": 2,  # Same - Same
                "transferMap": transfer_map
                }

        for n in range(3):
            rv = self.client.post('/api/v1/track-sample-step',
                                  data=json.dumps(data),
                                  content_type='application/json')
            assert rv.status_code == 200, rv.data
            result = json.loads(rv.data)
            assert result["success"] is True



if __name__ == '__main__':
    unittest.main()
