#!/bin/env python

import unittest
import os
import logging
logging.basicConfig(level=logging.INFO)

os.environ["WEBSITE_ENV"] = "Local"
# NOTE: because of the FLASK_APP.config.from_object(os.environ['APP_SETTINGS'])
# directive in the api code, importing the flask app must happen AFTER
# the os.environ Config above.
from app import app
from app import db


class TestCase(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        # assert "Unittest" in os.environ["WEBSITE_ENV"]
        assert 'localhost' in app.config['SQLALCHEMY_DATABASE_URI']
        assert 'postgres' in app.config['SQLALCHEMY_DATABASE_URI']
        db.create_all()

    def tearDown(self):
        # os.unlink(FLASK_APP.config['DATABASE'])  # delete filesystem sqlite
        pass

    def disabled_test_bug_flusherror(self):
        """ needs something other than an empty db """
        payload = {"sampleTransformTypeId":17,
                   "sampleTransformTemplateId":18,
                   "sourcePlates":["kipptest52",
                                   "kipptest53",
                                   "kipptest54",
                                   "kipptest55"],
                   "destinationPlates":["charlie7"]}
        rv = self.client.post('/api/v1/track-sample-step', data=payload)
        assert rv.status_code == 404
        """ was getting:     state_str(existing)))
FlushError: New instance <TransformDetail at 0x112848990> with identity key (<class 'app.dbmodels.TransformDetail'>, (186, 1)) conflicts with persistent instance <TransformDetail at 0x11be20ed0>"""

    def disabled_test_get_samples(self):
        rv = self.client.get('/samples')
        assert rv.status_code == 200
        # assert rv.data == '[]'

if __name__ == '__main__':
    unittest.main()
