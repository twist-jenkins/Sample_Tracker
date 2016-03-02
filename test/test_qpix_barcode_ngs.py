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
from app import login_manager

from test_flask_app import AutomatedTestingUser, rnd_bc
# from test_flask_app import RootPlate

EXAMPLE_NGS_BARCODING_SPEC = {
    "type":"PLATE_PLANNING",
    "title":"NGS Index hitpicking",
    "sources":[{
        "id":None,
        "type":"plate",
        "details":{
            "text":"",
            "id":"NGS_BARCODE_PLATE_TEST2",
            "plateDetails":{
                "type":"SPTT_0006",
                "createdBy":"Charlie Ledogar",
                "dateCreated":"2015-11-21 17:59:00"
            }
        }
    }],
    "destinations":[{
        "id":None,
        "type":"plate",
        "details":{
            "text":"",
            "id":"pEXT_test_Vh3va9Aq_13"
        }
    }],
    "operations":[{}],
    "details":{
        "text":"NGS Index hitpicking",
        "transform_template_id":30,
        "source_plate_count":1,
        "id":26,
        "destination_plate_count":0,
        "uid_group":10,
        "transform_type_id":26
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
    "destinations": None,
    "operations":[
        {
            "source_plate_barcode":"SRN 000577 SM-21",
            "source_well_name":"A1",
            "source_well_number": 1,
            "source_sample_id":"GA_562a647b799305708a87982f",
            "destination_plate_barcode":"f8m938fm3984y9834y",
            "destination_well_name":"A1",
            "destination_well_number": 1,
            "destination_plate_type": "SPTT_0006",
            "destination_plate_well_count":48
        }, {
            "source_plate_barcode":"SRN 000577 SM-21",
            "source_well_name":"A2",
            "source_well_number": 2,
            "source_sample_id":"GA_562a647b799305708a87982d",
            "destination_plate_barcode":"f8m938fm3984y9834y",
            "destination_well_name":"A2",
            "destination_well_number": 2,
            "destination_plate_type": "SPTT_0006",
            "destination_plate_well_count":48
        }
    ],
    "details":{
        "transform_template_id":1,
        "text":"Aliquoting for Quantification (384 plate)",
        "source_plate_count":1,
        "id":1,
        "destination_plate_count":1,
        "transform_type_id":1
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
        # db.create_all()
        cls.root_plate_barcode = 'SRN 000577 SM-30'  # qtray
        # cls.root_plate_barcode = RootPlate().create_in_db("XFER_ROOT",
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
        transform_map = [{
            "source_plate_barcode": self.root_plate_barcode,
            "source_well_name": src_well,
            "source_well_number": src_number,
            "destination_plate_barcode": dest_plate,
            "destination_well_name": dest_well,
            "destination_well_number": dest_number,
            "destination_plate_type": "SPTT_0005",
            "destination_plate_well_count": dest_well_count
        } for (src_well, src_number, dest_plate, dest_well,
               dest_number, dest_well_count) in [
            ('A1', 1, dest_plate_1_barcode, 'A1', 1, 96),
            ('A1', 1, dest_plate_1_barcode, 'A2', 2, 96),
            ('A2', 2, dest_plate_1_barcode, 'B1', 13, 96),
            ('B1', 25, dest_plate_2_barcode, 'A1', 1, 96),
            ('B1', 25, dest_plate_2_barcode, 'A2', 2, 96),
        ]]
        data = {"sampleTransformTypeId": 15,  # QPix To 96 plates
                "sampleTransformTemplateId": 21,
                "transformMap": transform_map
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
        transform_map = [{
            "source_plate_barcode": self.root_plate_barcode,
            "source_well_name": src_well,
            "source_well_number": src_number,
            "destination_plate_barcode": dest_plate,
            "destination_well_name": dest_well,
            "destination_well_number": dest_number,
            "destination_plate_type": "SPTT_0005",
            "destination_plate_well_count": dest_well_count
        } for (src_well, src_number, dest_plate, dest_well,
               dest_number, dest_well_count) in [
            ('A1', 1, dest_plate_1_barcode, 'A1', 1, 96),
            ('A1', 1, dest_plate_1_barcode, 'A2', 2, 96),
            ('A2', 2, dest_plate_1_barcode, 'B1', 13, 96),
            ('B1', 13, dest_plate_2_barcode, 'A1', 1, 96),
            ('B1', 13, dest_plate_2_barcode, 'A2', 2, 96),
        ]]

        data = {"sampleTransformTypeId": 26,  # NGS Prep: Barcode Hitpicking
                "sampleTransformTemplateId": 21,
                "transformMap": transform_map
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

    def test_v2_ngs_prep_golden(self):
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
        transform_map = [{
            "source_plate_barcode": self.root_plate_barcode,
            "source_well_name": src_well,
            "source_well_number": src_number,
            "destination_plate_barcode": dest_plate,
            "destination_well_name": dest_well,
            "destination_well_number": dest_number,
            "destination_plate_type": "SPTT_0005",
            "destination_plate_well_count": dest_well_count
        } for (src_well, src_number, dest_plate, dest_well,
               dest_number, dest_well_count) in [
            ('A1', 1, dest_plate_1_barcode, 'A1', 1, 96),
            ('A1', 1, dest_plate_1_barcode, 'A2', 2, 96),
            ('A2', 2, dest_plate_1_barcode, 'B1', 13, 96),
            ('B1', 13, dest_plate_2_barcode, 'A1', 1, 96),
            ('B1', 13, dest_plate_2_barcode, 'A2', 2, 96),
        ]]

        data = {"sampleTransformTypeId": 26,  # NGS Prep: Barcode Hitpicking
                "sampleTransformTemplateId": 21,
                "transformMap": transform_map
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

    def test_small_ngs_prep_golden_renamed(self):
        rnd = rnd_bc()
        dest_plate_1_barcode = rnd + '_1'
        dest_plate_2_barcode = rnd + '_2'

        transform_map = [{
            "source_plate_barcode": self.root_plate_barcode,
            "source_well_name": src_well,
            "source_well_number": src_number,
            "destination_plate_barcode": dest_plate,
            "destination_well_name": dest_well,
            "destination_well_number": dest_number,
            "destination_plate_type": "SPTT_0005",
            "destination_plate_well_count": dest_well_count
        } for (src_well, src_number, dest_plate, dest_well,
               dest_number, dest_well_count) in [
            ('A1', 1, dest_plate_1_barcode, 'A1', 1, 96),
            ('A1', 1, dest_plate_1_barcode, 'A2', 2, 96),
            ('A2', 2, dest_plate_1_barcode, 'B1', 13, 96),
            ('B1', 13, dest_plate_2_barcode, 'A1', 1, 96),
            ('B1', 13, dest_plate_2_barcode, 'A2', 2, 96),
        ]]

        data = {"sampleTransformTypeId": 26,  # NGS Prep: Barcode Hitpicking
                "sampleTransformTemplateId": 21,
                "transformMap": transform_map
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

    def test_small_ngs_barcoding_spec_golden(self):
        rnd = rnd_bc()
        dest_plate_1_barcode = rnd + '_1'
        dest_plate_2_barcode = rnd + '_2'
        root_cs_id = "CS_563bff9150a77622447fc8f5"

        test_fixture = [
            ['A1', 1, dest_plate_1_barcode, 'A1', 1, 96],
            ['A1', 1, dest_plate_1_barcode, 'A2', 2, 96],
            ['A2', 2, dest_plate_1_barcode, 'B1', 13, 96],
            # ['B1', 13, dest_plate_2_barcode, 'A1', 1, 96],
            # ['B1', 13, dest_plate_2_barcode, 'A2', 2, 96],
        ]

        # 1. Create two target plates
        transform_map = [{
            "source_plate_barcode": self.root_plate_barcode,
            "source_well_name": src_well,
            "source_well_number": src_number,
            "destination_plate_barcode": dest_plate,
            "destination_well_name": dest_well,
            "destination_well_number": dest_number,
            "destination_plate_type": "SPTT_0005",
            "destination_plate_well_count": dest_well_count
        } for (src_well, src_number, dest_plate, dest_well,
               dest_number, dest_well_count) in test_fixture]

        data = {"sampleTransformTypeId": 13,  # ?
                "sampleTransformTemplateId": 14,  # ?
                "transformMap": transform_map
                }
        rv = self.client.post('/api/v1/track-sample-step',
                              data=json.dumps(data),
                              content_type='application/json')
        assert rv.status_code == 200, rv.data
        result = json.loads(rv.data)
        assert result["success"] is True

        # 2. read the sample IDs

        ancestor_sample_ids = set()
        for ix, (src_well, src_number, dest_plate, dest_well,
             dest_number, dest_well_count) in enumerate(test_fixture):
            rv = self.client.get('/api/v1/rest/plate/%s/well/%d' %
                                 (dest_plate, dest_number),
                                 content_type='application/json')
            assert rv.status_code == 200, rv.data
            result = json.loads(rv.data)
            assert result["errors"] == []
            sample_id = result["data"]["id"]
            test_fixture[ix].append(sample_id)
            ancestor_sample_ids.add(sample_id)

        # 3. create an ngs barcoding spec (type 26)

        spec = EXAMPLE_NGS_BARCODING_SPEC.copy()
        plate_barcodes = set([el[2] for el in test_fixture])
        spec["destinations"] = [{"id": None, "type": "plate",
                                 "details": {"text": "", "id": plate_barcode}}
                                for plate_barcode in plate_barcodes]

        # 4. post the spec -- this replaces post('/api/v1/track-sample-step')

        rv = self.client.post('/api/v1/rest/transform-specs',
                              data=json.dumps({"plan": spec}),
                              content_type='application/json')
        assert rv.status_code == 201, rv.data
        new_spec_url = rv.headers['location']

        # 5. the spec should now exist but not be executed yet

        result = json.loads(rv.data)
        assert "data" in result
        assert "data_json" in result["data"]
        assert result["data"]["date_executed"] is None

        # 6. the spec should have BCS_ going in and nothing going out

        operations = result["data"]["data_json"]["operations"]
        for oper in operations:
            assert oper["source_sample_id"][0:4] == "BCS_"
            assert "destination_sample_id" not in oper

        # 7. We should be able to get an echo worklist

        echo_url = new_spec_url + ".echo.csv"
        rv = self.client.get(echo_url,
                             content_type="application/json")
        assert rv.status_code == 200
        import csv
        echo_csv = list(csv.DictReader(rv.data.splitlines()))
        assert len(echo_csv) == len(transform_map) * 2
        for line in echo_csv:
            assert line["Source Plate Barcode"] == "NGS_BARCODE_PLATE_TEST2"
            assert line["Destination Plate Barcode"] in (dest_plate_1_barcode,
                                                         dest_plate_2_barcode)

        # 8. Now execute

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

        # 9. Now make sure the samples are barcoded
        from collections import defaultdict
        bc_pairs = defaultdict(int)
        for ix, well in enumerate(operations):
            # target_id = well["destination_sample_id"]
            target_well_number = well["destination_well_number"]
            # assert target_id[0:4] == "NPS_"
            barcode_sample_id = well["source_sample_id"]
            assert barcode_sample_id[0:4] == "BCS_"
            barcode_sequence_id = 'BC_' + barcode_sample_id[4:]
            rv = self.client.get('/api/v1/rest/plate/%s/well/%d'
                                 % (dest_plate_1_barcode, target_well_number),
                                 content_type='application/json')
            assert rv.status_code == 200, rv.data
            result = json.loads(rv.data)
            assert "data" in result
            dat = result["data"]
            print "$" * 80, dat
            assert len(dat["parents"]) == 1
            assert dat["parents"][0] in ancestor_sample_ids
            if ix % 2:
                assert dat["i5_sequence_id"] == barcode_sequence_id
            else:
                assert dat["i7_sequence_id"] == barcode_sequence_id
                bc_pairs[(dat["i5_sequence_id"], dat["i7_sequence_id"])] += 1

        # 10. Make sure there are the expected number of unique pairs
        assert len(bc_pairs) == len(transform_map)

    def DISABLED_test_pooling(self):
        # 11. We should be able to get a miseq sample sheet
        # 'https://sampletransfer-stg.twistbioscience.com/api/v1/rest/transform-specs/194.miseq.csv'
        new_spec_url = 'FIXME'
        miseq_csv_url = new_spec_url + ".miseq.csv"
        rv = self.client.get(miseq_csv_url,
                             content_type="application/json")
        assert rv.status_code == 200
        result = json.loads(rv.data)
        assert 'Amplicon' in result


if __name__ == '__main__':
    unittest.main()
