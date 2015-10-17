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
        cls.root_plate_barcode = RootPlate().create_in_db("PLAN_ROOT",
                                                          db.engine)

    @classmethod
    def tearDownClass(cls):
        # cls._connection.destroy()
        # os.unlink(FLASK_APP.config['DATABASE'])  # delete filesystem sqlite
        pass

    def test_get_list_golden(self):
        rv = self.client.get('/api/v1/rest/transfer-plans')
        assert rv.status_code == 200
        result = json.loads(rv.data)
        assert len(result) > 0

    def test_get_one_golden(self):
        rv = self.client.get('/api/v1/rest/transfer-plans/plan_1')
        assert rv.status_code == 200
        result = json.loads(rv.data)
        assert len(result) == 1

    def test_get_one_404(self):
        rv = self.client.get('/api/v1/rest/transfer-plans/waldo')
        assert rv.status_code == 404

    def test_post_get_golden(self):
        new_plan = {"task": "new_task_1"}
        rv = self.client.post('/api/v1/rest/transfer-plans',
                              data=json.dumps(new_plan),
                              content_type="application/json")
        assert rv.status_code == 201
        new_uri = rv.headers['location']
        assert new_uri is not None

        result = json.loads(rv.data)
        assert result == new_plan  # this might be too heavy

        rv2 = self.client.get(new_uri)
        assert rv2.status_code == 200
        result2 = json.loads(rv2.data)
        assert len(result2) == 1

    def test_put_get_golden(self):
        modified_plan = {"task": "modified_task_1"}
        uri = '/api/v1/rest/transfer-plans/plan_1'
        rv = self.client.put(uri,
                             data=json.dumps(modified_plan),
                             content_type="application/json")
        assert rv.status_code == 201
        new_url = rv.headers['location']
        assert uri in new_url

        result = json.loads(rv.data)
        assert result == modified_plan  # this might be too heavy

        rv2 = self.client.get(uri)
        assert rv2.status_code == 200
        result2 = json.loads(rv2.data)
        assert len(result2) == 1
        assert rv2.data == rv.data


if __name__ == '__main__':
    unittest.main()
