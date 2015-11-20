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

EXAMPLE_BARCODING_SPEC = {
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

EXAMPLE_ALIQUOT_SPEC = {
    "type":"plate_step",
    "title":"Aliquoting for Quantification (384 plate)",
    "sources":[{
        "id":None,
        "type":"plate",
        "details":{
            "text":"",
            "id":"SRN 000577 SM-21",
            "plateDetails":{
                "type":"SPTT_0004",
                "createdBy":"Leslie Stanton",
                "dateCreated":"2015-11-08 14:38:42.182940"
            }
        }
    }],
    "destinations":[{
        "id":None,
        "type":"plate",
        "details":{
            "text":"","id":"f8m938fm3984y9834y"
        }
    }],
    "operations":[
        {
            "source_plate_barcode":"SRN 000577 SM-21","source_well_name":"A1","source_sample_id":"GA_562a647b799305708a87982f","destination_plate_barcode":"f8m938fm3984y9834y","destination_well_name":"A1","destination_plate_well_count":48
        }, {
            "source_plate_barcode":"SRN 000577 SM-21","source_well_name":"A2","source_sample_id":"GA_562a647b799305708a87982d","destination_plate_barcode":"f8m938fm3984y9834y","destination_well_name":"A2","destination_plate_well_count":48
        }
    ],
    "details":{
        "transfer_template_id":1,
        "text":"Aliquoting for Quantification (384 plate)",
        "source_plate_count":1,
        "id":1,
        "destination_plate_count":1,
        "transfer_type_id":1
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

    def test_small_aliquot_spec_golden(self):
        spec = EXAMPLE_ALIQUOT_SPEC.copy()
        rnd = rnd_bc()
        dest_plate_barcode = rnd + '_1'
        transfer_map = [{
            "source_plate_barcode": self.root_plate_barcode,
            "source_well_name": src_well,
            "destination_plate_barcode": dest_plate,
            "destination_well_name": dest_well,
            "destination_plate_well_count": dest_well_count,
            "source_sample_id": "CS_563fd11f785b1a7dd06dc817"
        } for (src_well, dest_plate, dest_well, dest_well_count) in [
            ('A1', dest_plate_barcode, 'A1', 48),
            ('A2', dest_plate_barcode, 'A2', 48),
            ('B1', dest_plate_barcode, 'B1', 48),
            ('B2', dest_plate_barcode, 'B2', 48),
            ('C1', dest_plate_barcode, 'C1', 48),
        ]]
        spec["operations"] = transfer_map

        # post the spec -- this replaces post('/api/v1/track-sample-step')

        headers = [("Transform-Execution", "Immediate")]
        rv = self.client.post('/api/v1/rest/transform-specs',
                              data=json.dumps({"plan": spec}),
                              content_type='application/json',
                              headers=headers)
        assert rv.status_code == 201, rv.data

        # the spec should now exist but not be executed yet

        result = json.loads(rv.data)
        assert "data" in result
        assert "data_json" in result["data"]
        assert result["data"]["date_executed"] is not None

        # there should be a plate already

        rv = self.client.get('/api/v1/basic-plate-info/%s'
                             % dest_plate_barcode,
                             content_type='application/json')
        assert rv.status_code == 200, rv.data
        result = json.loads(rv.data)
        print result
        assert result["success"] is True

    def test_small_ngs_barcoding_spec_golden(self):
        spec = EXAMPLE_BARCODING_SPEC.copy()
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

        # 1. post the spec -- this replaces post('/api/v1/track-sample-step')

        rv = self.client.post('/api/v1/rest/transform-specs',
                              data=json.dumps({"plan": spec}),
                              content_type='application/json')
        assert rv.status_code == 201, rv.data
        new_spec_url = rv.headers['location']

        # 2. the spec should now exist but not be executed yet

        result = json.loads(rv.data)
        assert "data" in result
        assert "data_json" in result["data"]
        assert result["data"]["date_executed"] is None

        # 3. the spec should have some foo

        operations = result["data"]["data_json"]["operations"]
        for well in operations:
            assert well["source_sample_id"][0:3] == "BC_"
            assert well["destination_sample_id"][0:4] == "NPS_"

        # 4. there should be no plate yet

        rv = self.client.get('/api/v1/basic-plate-info/%s'
                             % dest_plate_1_barcode,
                             content_type='application/json')
        assert rv.status_code == 404, rv.data

        # 5. We should be able to get an echo worklist

        # 6. Now execute

        # properly:
        # headers = [("Transform-Execution", "Immediate")]
        # rv = self.client.put(new_spec_url,
        #                      content_type="application/json",
        #                      headers=headers)
        # assert rv.status_code == 200

        # hackily:
        execute_url = new_spec_url + ".execute"
        rv = self.client.get(execute_url,
                             content_type="application/json")

        assert rv.status_code == 200
        result = json.loads(rv.data)
        data = result["data"]

        date_executed = data["date_executed"]
        assert date_executed is not None

        # 7. there should now be a plate

        rv = self.client.get('/api/v1/basic-plate-info/%s'
                             % dest_plate_1_barcode,
                             content_type='application/json')
        assert rv.status_code == 200, rv.data

if __name__ == '__main__':
    unittest.main()
