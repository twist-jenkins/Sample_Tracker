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

EXAMPLE_SPEC = {
    "type":"plate_step",
    "title":"NGS prep: barcode hitpicking",
    "sources":[{
        "id": None,
        "type":"plate",
        "details":{
            "text":"",
            "id":"SRN 000000 SM-37",
            "plateDetails":{
                "type":"SPTT_0006",
                "createdBy":"Charlie Ledogar",
                "dateCreated":"2015-11-08 14:47:55.714115"
                }
            }
        }
    ],
    "destinations":[],
    "operations":[
        {
            "source_plate_barcode":"SRN 000577 SM-37",
            "source_well_name":"K13",
            "source_sample_id":"CS_563fd11f785b1a7dd06dc817",
            "destination_plate_barcode":"SRN 000577 SM-37",
            "destination_well_name":"K13",
            "destination_plate_well_count":384
        },{
            "source_plate_barcode":"SRN 000577 SM-37",
            "source_well_name":"K15",
            "source_sample_id":"CS_563fd11f785b1a7dd06dc819",
            "destination_plate_barcode":"SRN 000577 SM-37",
            "destination_well_name":"K15",
            "destination_plate_well_count":384
        }
    ],
    "details":{
        "transfer_template_id":2,
        "text":"NGS prep: barcode hitpicking",
        "source_plate_count":1,"id":26,
        "destination_plate_count":0,
        "transfer_type_id":26
    }
}

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

        rv = self.client.get('/api/v1/basic-plate-info/%s'
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

        rv = self.client.get('/api/v1/basic-plate-info/%s'
                             % dest_plate_1_barcode,
                             content_type='application/json')
        assert rv.status_code == 200, rv.data
        result = json.loads(rv.data)
        print result
        assert result["success"] is True

    def disabled_test_v2_ngs_prep_golden(self):
        """ This test should:
        1. create a new pair of CS plates using Qpix as above
        2. using special barcode plate as source, and
           that pair of CS plates as destination, create but
           do not execute a transform spec, using up barcodes
           from the sequence, but potentially not yet creating
           NPS instances
        3. download the transform spec as echo worklist
        4. execute the transform spec, which should create the
           NPS instances
        """
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

        rv = self.client.get('/api/v1/basic-plate-info/%s'
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

        rv = self.client.get('/api/v1/basic-plate-info/%s'
                             % dest_plate_1_barcode,
                             content_type='application/json')
        assert rv.status_code == 200, rv.data
        result = json.loads(rv.data)
        print result
        assert result["success"] is True

    def test_small_ngs_prep_spec_golden(self):
        spec = EXAMPLE_SPEC.copy()
        rnd = rnd_bc()
        dest_plate_1_barcode = rnd + '_1'
        dest_plate_2_barcode = rnd + '_2'
        transfer_map = [{
            "source_plate_barcode": self.root_plate_barcode,
            "source_well_name": src_well,
            "destination_plate_barcode": dest_plate,
            "destination_well_name": dest_well,
            "destination_plate_well_count": dest_well_count,
            "source_sample_id": "CS_563fd11f785b1a7dd06dc817"
        } for (src_well, dest_plate, dest_well, dest_well_count) in [
            ('A1', dest_plate_1_barcode, 'A1', 96),
            ('A1', dest_plate_1_barcode, 'A2', 96),
            ('A2', dest_plate_1_barcode, 'B1', 96),
            ('B1', dest_plate_2_barcode, 'A1', 96),
            ('B1', dest_plate_2_barcode, 'A2', 96),
        ]]
        spec["operations"] = transfer_map
        spec["details"] = {
            "transfer_template_id": 2,  # 21?
            "text": "NGS prep: barcode hitpicking",
            "source_plate_count": 1,
            "id": 26,
            "destination_plate_count": 0,
            "transfer_type_id": 26
        }

        # post the spec -- this replaces post('/api/v1/track-sample-step')

        rv = self.client.post('/api/v1/rest/transform-specs',
                              data=json.dumps({"plan": spec}),
                              content_type='application/json')
        assert rv.status_code == 201, rv.data

        # the spec should now exist but not be executed yet

        result = json.loads(rv.data)
        assert "data" in result
        assert "data_json" in result["data"]
        assert result["data"]["date_executed"] is None

        # the spec should have some foo
        assert result["data"]["data_json"]["foo"] == "bar"

        # there should be no plate yet

        rv = self.client.get('/api/v1/basic-plate-info/%s'
                             % dest_plate_1_barcode,
                             content_type='application/json')
        assert rv.status_code == 404, rv.data





if __name__ == '__main__':
    unittest.main()
