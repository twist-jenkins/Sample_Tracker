"""Confirm that we can produce a worklist for hitpicking."""

import unittest
from app import app
from app import db
from app.utils import scoped_session

from app import login_manager

from test_flask_app import AutomatedTestingUser

from twistdb.sampletrack import Plate

class TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        login_manager.anonymous_user = AutomatedTestingUser
        cls.client = app.test_client()
        assert 'localhost' in app.config['SQLALCHEMY_DATABASE_URI']
        assert 'postgres' in app.config['SQLALCHEMY_DATABASE_URI']
        cls.root_plate_barcode = 'SRN 000577 SM-30'  # qtray

    @classmethod
    def tearDownClass(cls):
        # cls._connection.destroy()
        # os.unlink(FLASK_APP.config['DATABASE'])  # delete filesystem sqlite
        pass

    def test_plate_query(self):
        with scoped_session(db.engine) as session:
            res = session.query(Plate).get('FAKE_QPIX_OUT')
            assert len(res.current_well_contents(session)) == 3  # Should have 3 samples

            for sample in res.current_well_contents(session):
                if sample.id in ['S_PASS_QPIX_PARENT', 'S_NONROI_QPIX_PARENT']:
                    assert sample.passed_ngs

                if sample.id == 'S_PASS_QPIX_PARENT':
                    assert sample.is_best_clone

                if sample.id == 'S_TERRIBLE_QPIX_PARENT':
                    assert sample.is_best_clone is False
                    assert sample.passed_ngs is False
