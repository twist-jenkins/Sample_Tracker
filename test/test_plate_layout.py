import unittest
import logging
logging.basicConfig(level=logging.INFO)

# from flask_login import AnonymousUserMixin

# os.environ["WEBSITE_ENV"] = "Local"

# NOTE: because of the FLASK_APP.config.from_object(os.environ['APP_SETTINGS'])
# directive in the api code, importing the flask app must happen AFTER
# the os.environ Config above.

import sys
print '@@', sys.path

from app import app
from app import db
from app.utils import scoped_session

from twistdb.sampletrack import Plate
from test_flask_app import rnd_bc


class TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        assert 'localhost' in app.config['SQLALCHEMY_DATABASE_URI']
        assert 'postgres' in app.config['SQLALCHEMY_DATABASE_URI']
        print '@@', app.config['SQLALCHEMY_DATABASE_URI']
        # cls.qtray_barcode = 'SRN 000577 SM-30'  # qtray
        cls.operator_id = 'cledogar'

    @classmethod
    def tearDownClass(cls):
        pass

    def test_qtray_layout(self):
        plate_id = rnd_bc()
        plate_type_id = "SPTT_0004"
        with scoped_session(db.engine) as db_session_1:
            plate_in = Plate(id=plate_id,
                             type_id=plate_type_id,
                             operator_id=self.operator_id,
                             )
            db_session_1.add(plate_in)

        with scoped_session(db.engine) as db_session_2:
            plate_out = db_session_2.query(Plate).filter_by(id=plate_id).one()
            assert plate_out is not None
            assert plate_out.type_id == plate_type_id
            assert plate_out.plate_type.name == '48 well, plastic (QTray)'

            layout = plate_out.plate_type.layout

            assert layout.get_well_name(1) == 'A1'
            assert layout.get_well_name(6) == 'A6'
            assert layout.get_well_name(7) == 'B1'
            assert layout.get_well_name(8) == 'B2'
            assert layout.get_well_name(9) == 'B3'
            assert layout.get_well_name(10) == 'B4'
            assert layout.get_well_name(48) == 'H6'

    def test_384_well_layout(self):
        plate_id = rnd_bc()
        plate_type_id = "SPTT_0006"
        with scoped_session(db.engine) as db_session_1:
            plate_in = Plate(id=plate_id,
                             type_id=plate_type_id,
                             operator_id=self.operator_id,
                             )
            db_session_1.add(plate_in)

        with scoped_session(db.engine) as db_session_2:
            plate_out = db_session_2.query(Plate).filter_by(id=plate_id).one()
            assert plate_out is not None
            assert plate_out.type_id == plate_type_id
            assert plate_out.plate_type.name == '384 well, plastic'

            layout = plate_out.plate_type.layout

            assert layout.get_well_name(1) == 'A1'
            assert layout.get_well_name(24) == 'A24'
            assert layout.get_well_name(25) == 'B1'
            assert layout.get_well_name(384) == 'P24'


if __name__ == '__main__':
    unittest.main()
