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


class TestCase(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        assert "Unittest" in os.environ["WEBSITE_ENV"]
        assert '@' not in app.config['SQLALCHEMY_DATABASE_URI']
        assert 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']

    def tearDown(self):
        # os.unlink(FLASK_APP.config['DATABASE'])
        pass

    def test_get_404(self):
        rv = self.client.get('/testing_404_1982341982374')
        assert rv.status_code == 404

    def disabled_test_get_samples(self):
        rv = self.client.get('/samples')
        assert rv.status_code == 200
        assert rv.data == "foo"

    """
    def test_scores_calculate_test3(self):
        with open("tests/tests_data/scoring/test3.json") as json_file:
            data = json_file.read()
            rv = self.client.post('/scores/calculate', data=data,
                                  content_type='application/json')
        assert rv.status_code == 200
        response_json = json.loads(rv.data)
        assert len(response_json["scores"]) == 4
        # assert response_json == { ['score']}
        # scores = [el["score"] for el in response_json["scores"]]
        # assert scores == [5, 5, 5, 5]
        assert response_json["scores"][0] == {'score': 5}
        assert 'error' in response_json["scores"][1]
        assert response_json["scores"][2] == {'score': 5}
        assert 'error' in response_json["scores"][3]
    """

if __name__ == '__main__':
    unittest.main()
