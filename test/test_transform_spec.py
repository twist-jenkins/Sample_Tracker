#!/bin/env python

import unittest
import json
import os
import logging
logging.basicConfig(level=logging.INFO)

# os.environ["WEBSITE_ENV"] = "Localunittest"

# NOTE: because of the FLASK_APP.config.from_object(os.environ['APP_SETTINGS'])
# directive in the api code, importing the flask app must happen AFTER
# the os.environ Config above.
from app import app
from app import db
from app import login_manager

from test_flask_app import AutomatedTestingUser, RootPlate
# from sqlalchemy.exc import IntegrityError


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
        assert len(result) == 1

    def test_get_one_404(self):
        rv = self.client.get('/api/v1/rest/transform-specs/0')
        assert rv.status_code == 404

    def test_post_get_golden(self):
        new_spec = {"task": "new_task_1"}
        rv = self.client.post('/api/v1/rest/transform-specs',
                              data=json.dumps(new_spec),
                              content_type="application/json")
        assert rv.status_code == 201
        new_url = rv.headers['location']
        assert new_url is not None
        result = json.loads(rv.data)
        assert new_spec in result.values()
        assert self.client.get(new_url).status_code == 200
        self.client.delete(new_url)

    def test_post_put_get_golden(self):
        new_spec = {"task": "delete_me"}
        uri = '/api/v1/rest/transform-specs'
        rv = self.client.post(uri,
                              data=json.dumps(new_spec),
                              content_type="application/json")
        assert rv.status_code == 201
        new_url = rv.headers['location']
        modified_spec = {"task": "modified_task_1"}
        rv = self.client.put(new_url,
                             data=json.dumps(modified_spec),
                             content_type="application/json")
        assert rv.status_code == 201
        new_url = rv.headers['location']
        assert uri in new_url
        result = json.loads(rv.data)
        assert modified_spec in result
        assert self.client.get(new_url).status_code == 200
        self.client.delete(new_url)

    def test_post_delete_golden(self):
        new_spec = {"task": "delete_me"}
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
        new_spec = {"foo": "bar"}
        rv = self.client.post('/api/v1/rest/transform-specs',
                              data=json.dumps(new_spec),
                              content_type="application/json")
        assert rv.status_code == 201
        new_url = rv.headers['location']
        assert new_url is not None
        result = json.loads(rv.data)
        assert new_spec in result
        assert self.client.get(new_url).status_code == 200
        self.client.delete(new_url)

    def test_get_list_golden(self):
        new_spec = {"foo": "bar"}
        rv = self.client.post('/api/v1/rest/transform-specs',
                              data=json.dumps(new_spec),
                              content_type="application/json")
        assert rv.status_code == 201
        new_url = rv.headers['location']

        rv = self.client.get('/api/v1/rest/transform-specs')
        assert rv.status_code == 200
        result = json.loads(rv.data)
        assert len(result) > 0
        assert new_spec in result.values()
        self.client.delete(new_url)

if __name__ == '__main__':
    unittest.main()
