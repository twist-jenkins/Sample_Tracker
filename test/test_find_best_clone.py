"""Confirm that we can pull best/passing clone annotation from NGS results."""

import unittest
from app import app
from app import db
from app.utils import scoped_session

from app import login_manager

from test_flask_app import AutomatedTestingUser

from twistdb.sampletrack import Sample
from twistdb.ngs import CallerSummary

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

    def test_ngs_results_in_sample(self):
        with scoped_session(db.engine) as session:
            res = session.query(CallerSummary).\
                filter(CallerSummary.sample_id == 'S_PASS_QPIX_PARENT',
                       CallerSummary.caller_stage == 'oi-roll-up').one()
            assert res.value['Passing Results'] == 2
            assert res.value['Best Clone'] == 'S_PASS_QPIX_PARENT'
            assert res.value['Alternate Clones'] == 'S_NONROI_QPIX_PARENT'

            # And test that the sample-level reference to selected clones works
            passer = session.query(Sample).get('S_PASS_QPIX_PARENT')
            assert passer.is_best_clone is True
            assert len(passer.caller_selection) == 1
            assert passer.passed_ngs is True
            assert len(passer.caller_passing) == 1

            # Make sure the accessor methods on a failing smaple return false
            failer = session.query(Sample).get('S_TERRIBLE_QPIX_PARENT')
            assert failer.is_best_clone is False
            assert failer.passed_ngs is False
