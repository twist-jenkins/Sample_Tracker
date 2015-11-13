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

from test_flask_app import AutomatedTestingUser, RootPlate, rnd_bc
# from sqlalchemy.exc import IntegrityError

EXAMPLE_SPEC = {
    "plan": {
        "type":"plate_step",
        "title":"Aliquoting for Quantification (384 plate)",
        "sources":[{"id":None,"type":"plate","details":{"text":"","id":"H3904Y1W","plateDetails":{"type":"SPTT_0006","createdBy":"Jackie Fidanza","dateCreated":"2015-08-17 10:19:06"}}}],
        "destinations":[{"id":None,"type":"plate","details":{"text":"","id":rnd_bc()}}],
        "operations":[
        {"source_plate_barcode":"H3904Y1W","source_well_name":"A5","source_sample_id":"GA_55d2178b799305dbef8bf2c7","destination_plate_barcode":"test34343452352","destination_well_name":"A5","destination_plate_well_count":384},
        {
        "source_plate_barcode":"H3904Y1W","source_well_name":"A6","source_sample_id":"GA_55d2178b799305dbef8bf2c6","destination_plate_barcode":"test34343452352","destination_well_name":"A6","destination_plate_well_count":384},
        {
        "source_plate_barcode":"H3904Y1W","source_well_name":"A7","source_sample_id":"GA_55d2178b799305dbef8bf2c5","destination_plate_barcode":"test34343452352","destination_well_name":"A7","destination_plate_well_count":384}
        ],
        "details":{"transfer_template_id":1,
                   "transfer_type_id":1,
                   "text":"Aliquoting for Quantification (384 plate)",
                   "source_plate_count":1,
                   "id":1,
                   "destination_plate_count":1}
    }
}

class TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        login_manager.anonymous_user = AutomatedTestingUser
        cls.client = app.test_client()
        # assert "Unittest" in os.environ["WEBSITE_ENV"]
        #assert 'localhost' in app.config['SQLALCHEMY_DATABASE_URI']
        assert 'postgres' in app.config['SQLALCHEMY_DATABASE_URI']
        db.create_all()
        try:
            cls.root_plate_barcode = RootPlate().create_in_db("PLAN_ROOT2",
                                                              db.engine)
        except: #  IndexError, IntegrityError:
            pass

    @classmethod
    def tearDownClass(cls):
        # cls._connection.destroy()
        # os.unlink(FLASK_APP.config['DATABASE'])  # delete filesystem sqlite
        pass


    def DISABLED_test_get_one_golden(self):
        rv = self.client.get('/api/v1/rest/transform-specs/100001')
        assert rv.status_code == 200
        result = json.loads(rv.data)
        data = result["data"]
        assert len(data) == 1

    def test_get_one_404(self):
        rv = self.client.get('/api/v1/rest/transform-specs/0')
        assert rv.status_code == 404

    def test_post_get_golden(self):
        new_spec = {"plan": {"task": "new_task_1"}}
        rv = self.client.post('/api/v1/rest/transform-specs',
                              data=json.dumps(new_spec),
                              content_type="application/json")
        assert rv.status_code == 201
        new_url = rv.headers['location']
        assert new_url is not None
        new_spec_id = new_url.split('/')[-1]
        assert int(new_spec_id) > 0
        new_spec_id = int(new_spec_id)

        result = json.loads(rv.data)
        data = result["data"]
        assert data["spec_id"] == new_spec_id
        assert data["data_json"] == new_spec["plan"]
        assert self.client.get(new_url).status_code == 200
        self.client.delete(new_url)

    def test_post_put_get_golden(self):
        """ needs refactor """
        new_spec = {"plan": {"task": "modify_me"}}
        uri = '/api/v1/rest/transform-specs'
        rv = self.client.post(uri,
                              data=json.dumps(new_spec),
                              content_type="application/json")
        assert rv.status_code == 201
        new_url = rv.headers['location']
        modified_spec = {"plan": {"task": "modified_task_1"}}
        rv = self.client.put(new_url,
                             data=json.dumps(modified_spec),
                             content_type="application/json")
        assert rv.status_code == 201
        new_url = rv.headers['location']
        assert uri in new_url
        result = json.loads(rv.data)
        data = result["data"]
        spec_id = data["spec_id"]

        rv = self.client.get('/api/v1/rest/transform-specs')
        assert rv.status_code == 200
        result = json.loads(rv.data)
        data = result["data"]
        assert len(data) > 0
        specs = {el["spec_id"]: el for el in data if "spec_id" in el}
        assert spec_id in specs.keys()
        assert specs[spec_id]["data_json"] == modified_spec["plan"]

        self.client.delete(new_url)
        assert self.client.get(new_url).status_code == 404

    def test_post_delete_golden(self):
        new_spec = {"plan": {"task": "delete_me"}}
        uri = '/api/v1/rest/transform-specs'
        rv = self.client.post(uri,
                              data=json.dumps(new_spec),
                              content_type="application/json")
        assert rv.status_code == 201
        new_url = rv.headers['location']
        assert new_url is not None
        assert self.client.get(new_url).status_code == 200

        assert self.client.delete(new_url).status_code == 204
        assert self.client.get(new_url).status_code == 404

    def test_post_get_2_golden(self):
        new_spec = {"plan": {"foo": "bar"}}
        rv = self.client.post('/api/v1/rest/transform-specs',
                              data=json.dumps(new_spec),
                              content_type="application/json")

        assert rv.status_code == 201
        new_url = rv.headers['location']
        assert new_url is not None
        result = json.loads(rv.data)
        data = result["data"]
        new_spec_id = data["spec_id"]

        assert data["data_json"] == new_spec["plan"]
        assert self.client.get(new_url).status_code == 200

        self.client.delete(new_url)
        assert self.client.get(new_url).status_code == 404

    def test_get_list_golden(self):
        new_spec = {"plan": {"foo": "bar"}}
        rv = self.client.post('/api/v1/rest/transform-specs',
                              data=json.dumps(new_spec),
                              content_type="application/json")
        assert rv.status_code == 201
        new_url = rv.headers['location']
        result = json.loads(rv.data)
        data = result["data"]
        spec_id = data['spec_id']

        rv = self.client.get('/api/v1/rest/transform-specs')
        assert rv.status_code == 200
        result = json.loads(rv.data)
        data = result["data"]
        assert len(data) > 0
        specs = {el["spec_id"]: el for el in data if "spec_id" in el}
        assert spec_id in specs.keys()
        assert specs[spec_id]["data_json"] == new_spec["plan"]

        self.client.delete(new_url)
        assert self.client.get(new_url).status_code == 404

    def test_post_default_execution_golden(self):
        """ targeting the execution method """
        new_spec = EXAMPLE_SPEC.copy()
        new_spec["plan"]["destinations"][0]["details"]["id"] = rnd_bc()
        uri = '/api/v1/rest/transform-specs'
        rv = self.client.post(uri,
                              data=json.dumps(new_spec),
                              content_type="application/json")
        assert rv.status_code == 201
        new_url = rv.headers['location']
        result = json.loads(rv.data)
        data = result["data"]

        date_executed = data["date_executed"]
        assert date_executed is None

        self.client.delete(new_url)
        assert self.client.get(new_url).status_code == 404

    def test_post_immediate_execution_golden(self):
        """ targeting the execution method """
        new_spec = EXAMPLE_SPEC.copy()
        new_spec["plan"]["destinations"][0]["details"]["id"] = rnd_bc()
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

        self.client.delete(new_url)
        assert self.client.get(new_url).status_code == 404

    def test_post_deferred_execution_golden(self):
        """ targeting the execution method """
        new_spec = EXAMPLE_SPEC.copy()
        new_spec["plan"]["destinations"][0]["details"]["id"] = rnd_bc()
        uri = '/api/v1/rest/transform-specs'
        headers = [("Transform-Execution", "Deferred")]
        rv = self.client.post(uri,
                              data=json.dumps(new_spec),
                              content_type="application/json",
                              headers=headers)
        assert rv.status_code == 201
        new_url = rv.headers['location']

        headers = [("Transform-Execution", "Immediate")]
        rv = self.client.put(new_url,
                             data=json.dumps(new_spec),
                             content_type="application/json",
                             headers=headers)
        assert rv.status_code == 201
        result = json.loads(rv.data)
        data = result["data"]

        date_executed = data["date_executed"]
        assert date_executed is not None

        self.client.delete(new_url)
        assert self.client.get(new_url).status_code == 404

if __name__ == '__main__':
    unittest.main()
