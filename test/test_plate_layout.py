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

            assert plate_out.get_well_by_number(1).well_label == 'A1'
            assert plate_out.get_well_by_number(6).well_label == 'A6'
            assert plate_out.get_well_by_number(7).well_label == 'B1'
            assert plate_out.get_well_by_number(8).well_label == 'B2'
            assert plate_out.get_well_by_number(9).well_label == 'B3'
            assert plate_out.get_well_by_number(10).well_label == 'B4'
            assert plate_out.get_well_by_number(48).well_label == 'H6'

            assert plate_out.get_well_by_label('A1').well_number == 1
            assert plate_out.get_well_by_label('A6').well_number == 6
            assert plate_out.get_well_by_label('B1').well_number == 7
            assert plate_out.get_well_by_label('B2').well_number == 8
            assert plate_out.get_well_by_label('B3').well_number == 9
            assert plate_out.get_well_by_label('B4').well_number == 10
            assert plate_out.get_well_by_label('H6').well_number == 48

            layout = plate_out.plate_type.layout

            assert layout.get_well_by_number(1).well_label == 'A1'
            assert layout.get_well_by_number(6).well_label == 'A6'
            assert layout.get_well_by_number(7).well_label == 'B1'
            assert layout.get_well_by_number(8).well_label == 'B2'
            assert layout.get_well_by_number(9).well_label == 'B3'
            assert layout.get_well_by_number(10).well_label == 'B4'
            assert layout.get_well_by_number(48).well_label == 'H6'

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

            assert layout.get_well_by_number(1).well_label == 'A1'
            assert layout.get_well_by_number(24).well_label == 'A24'
            assert layout.get_well_by_number(25).well_label == 'B1'
            assert layout.get_well_by_number(384).well_label == 'P24'


if __name__ == '__main__':
    unittest.main()
