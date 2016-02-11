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


class TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        login_manager.anonymous_user = AutomatedTestingUser
        cls.client = app.test_client()
        assert 'postgres' in app.config['SQLALCHEMY_DATABASE_URI']

    @classmethod
    def tearDownClass(cls):
        # cls._connection.destroy()
        # os.unlink(FLASK_APP.config['DATABASE'])  # delete filesystem sqlite
        pass

    def test_titin_plate(self):
        """ should move to a different .py file """

        uri = '/api/v1/basic-plate-info/SRN-WARP1-TEST1'
        rv = self.client.get(uri,
                             content_type="application/json")
        assert rv.status_code == 200
        result = json.loads(rv.data)
        assert "wells" in result
        wells = result["wells"]

        # assert wells[6]['sample_id'] == 'GA_WARP1_TEST1_0007'
        assert wells[6]['column_and_row'] == '7'

        # assert wells[383]['sample_id'] == 'GA_WARP1_TEST1_0384'
        assert wells[383]['column_and_row'] == '384'

        # assert wells[384]['sample_id'] == 'GA_WARP1_TEST1_0385'
        assert wells[384]['column_and_row'] == '385'

        # assert wells[6143]['sample_id'] == 'GA_WARP1_TEST1_6144'
        assert wells[6143]['column_and_row'] == '6144'


if __name__ == '__main__':
    unittest.main()
