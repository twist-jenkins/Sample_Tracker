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

from test_flask_app import AutomatedTestingUser


class TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        login_manager.anonymous_user = AutomatedTestingUser
        cls.client = app.test_client()
        assert 'localhost' in app.config['SQLALCHEMY_DATABASE_URI']
        assert 'postgres' in app.config['SQLALCHEMY_DATABASE_URI']

    def test_plates_at_step_6(self):
        step = 6
        resp = self.client.get('/api/v1/rest/plates?ready_for_step=%d' % step,
                               content_type='application/json')
        assert resp.status_code == 200, resp.data
        result = json.loads(resp.data)
        print result
        assert result is not None

    def test_plates_at_all_steps(self):
        for step in range(51):
            resp = self.client.get('/api/v1/rest/plates?ready_for_step=%d'
                                   % step, content_type='application/json')
            assert resp.status_code == 200, resp.data
            result = json.loads(resp.data)
            print result
            assert result is not None

if __name__ == '__main__':
    unittest.main()
