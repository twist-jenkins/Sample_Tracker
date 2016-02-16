#!/bin/env python

import unittest
import json
import os
import logging
logging.basicConfig(level=logging.INFO)

# os.environ["WEBSITE_ENV"] = "Local"

# NOTE: because of the FLASK_APP.config.from_object(os.environ['APP_SETTINGS'])
# directive in the api code, importing the flask app must happen AFTER
# the os.environ Config above.
from app import app
from app import db
from app import login_manager
import json

from test_flask_app import AutomatedTestingUser, RootPlate, rnd_bc
# from sqlalchemy.exc import IntegrityError


def titin_extraction_spec():
    dest_plate_rootname = rnd_bc()
    spec = {
        "plan": {
                "destinations": [],
                "details": {
                    "destination_plate_count": 16,
                    "id": 52,
                    "source_plate_count": 1,
                    "text": "CHP Extraction - Titin",
                    "transfer_template_id": 34,
                    "transfer_type_id": 52,
                    "uid_group": 1
                },
                "operations": [
                ],
                "sources": [
                    {
                        "details": {
                            "id": "SRN-WARP1-TEST1",
                            "plateDetails": {
                                "createdBy": "Charlie Ledogar",
                                "dateCreated": "2016-01-17 00:00:00",
                                "type": "SPTT_1009"
                            },
                            "text": ""
                        },
                        "id": None,
                        "type": "plate"
                    }
                ],
                "title": "CHP Extraction - Titin",
                "type": "plate_step"
            },
            "date_created": "2016-02-11T13:19:12.726136",
            "date_executed": "2016-02-11T21:19:12.794893",
            "operator_id": "cledogar",
            "spec_id": 11,
            "status": None,
            "type_id": None

    }

    for extraction_num in range(16):
        if extraction_num % 4 != 0:  # only do 25% of the extractions
            continue
        plate_name = dest_plate_rootname + "_%02d" % (extraction_num + 1)
        detail = {
                        "details": {
                            "id": plate_name,
                            "plateDetails": {
                                "type": "SPTT_0006"
                            },
                            "text": ""
                        },
                        "id": None,
                        "type": "plate"
        }
        spec["plan"]["destinations"].append(detail)

        for well_384_id in range(384):
            if well_384_id % 100 != 0:  # only do 1% of the wells
                continue
            well_6144_id = 384 * extraction_num + well_384_id + 1
            well_6144_code = 661440000 + well_6144_id
            operation = {
                "destination_plate_barcode": plate_name,
                "destination_plate_type": "SPTT_0006",
                "destination_plate_well_count": 384,
                "destination_well_number": well_384_id + 1,
                "source_plate_barcode": "SRN-WARP1-TEST1",
                "source_sample_id": "GA_WARP1_TEST1_%04d" % well_6144_id,
                "source_well_code": well_6144_code,
                "source_well_number": well_6144_id
            }
            spec["plan"]["operations"].append(operation)

    return spec

class TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        login_manager.anonymous_user = AutomatedTestingUser
        cls.client = app.test_client()
        # assert "Unittest" in os.environ["WEBSITE_ENV"]
        #assert 'localhost' in app.config['SQLALCHEMY_DATABASE_URI']
        assert 'postgres' in app.config['SQLALCHEMY_DATABASE_URI']
        # db.create_all()
        try:
            cls.root_plate_barcode = RootPlate().create_in_db("PLAN_ROOT2",
                                                              db.engine)
        except:  #  IndexError, IntegrityError:
            pass

    @classmethod
    def tearDownClass(cls):
        # cls._connection.destroy()
        # os.unlink(FLASK_APP.config['DATABASE'])  # delete filesystem sqlite
        pass


    def test_post_immediate_execution_golden(self):
        """ targeting the execution method """
        new_spec = titin_extraction_spec()
        # new_spec["plan"]["destinations"][0]["details"]["id"] = rnd_bc()
        uri = '/api/v1/rest/transform-specs'
        headers = [("Transform-Execution", "Immediate")]
        rv = self.client.post(uri,
                              data=json.dumps(new_spec),
                              content_type="application/json",
                              headers=headers)
        assert rv.status_code == 201
        new_url = rv.headers['location']
        result = json.loads(rv.data)
        data = result["data"]

        date_executed = data["date_executed"]
        assert date_executed is not None

        dest_plate_names = [dest["details"]["id"]
                            for dest in new_spec["plan"]["destinations"]]

        for dest_plate_name in dest_plate_names:
            rv = self.client.get('/api/v1/basic-plate-info/%s'
                                 % dest_plate_name,
                                 content_type='application/json')
            assert rv.status_code == 200, rv.data
            result = json.loads(rv.data)
            print result
            assert result["success"] is True

        # self.client.delete(new_url)
        # assert self.client.get(new_url).status_code == 404


if __name__ == '__main__':
    unittest.main()
