import unittest
import logging
import math
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
from twistdb.sampletrack import Sample
from test_flask_app import rnd_bc


class TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        assert 'localhost' in app.config['SQLALCHEMY_DATABASE_URI']
        assert 'postgres' in app.config['SQLALCHEMY_DATABASE_URI']
        print '@@', app.config['SQLALCHEMY_DATABASE_URI']
        # cls.qtray_barcode = 'SRN 000577 SM-30'  # qtray
        cls.operator_id = 'sbanerjee'

    @classmethod
    def tearDownClass(cls):
        pass



    def test_getSamples(self):

        with scoped_session(db.engine) as db_session_2:
           # print 'session2'
           # plate_out = db_session_2.query(Plate).filter_by(id=plate_id).one()
            samples= db_session_2.query(Plate).filter(Plate.external_barcode  == 'PLT_PCA_NORM_TEST').one().current_well_contents
            #samples= db.session.query(Sample).filter(Sample.plate_id  == plate_id)
           # print len(samples)
            assert len(samples) is not None





    def test_calculate_volume_foreach_sample(self):
        with scoped_session(db.engine) as db_session_2:

            amp_d={}
            kan_d={}
            chlor_d={}
            unknown={}

            samples= db.session.query(Plate).filter(Plate.external_barcode  == 'PLT_WARP2.1').one().current_well_contents


            dest_type = db.session.query(PlateType).get('SPTT_0006')
            for src in enumerate(request.json['sources']) :
                plate_barcode = src['details']['id']
                samples =get_samples_fromeach_384well_plate(plate_barcode)

                for sample in samples:
                    concentration = sample.conc_ng_ul
                    cloning_process= sample.order_item.cloning_process
                    sequence = sample.order_item.sequence
                    if len(sequence) < 200 and (concentration is not  None):
                        fmol = 13*5
                        volume = (fmol/concentration)
                    elif len(sequence) >= 200 and (concentration is not  None) :
                        fmol = 13*2
                        volume = (fmol/concentration)

                        if cloning_process is not None :
                            marker = cloning_process.resistance_marker.code
                            if(marker == "AMP") :
                                amp_d.update({sample:volume});
                            elif(marker == "KAN")  :
                               kan_d.update({sample,volume});
                            elif(marker == 'CHLOR') :
                               chlor_d.update({sample,volume});
                            elif (marker is None) :
                                unknown.update(sample.volume);

            number= sum([len(amp_d),len(kan_d) ,len(chlor_d) ,len(unknown)])
            print (number/48) +1




    def test_create_worklist(self):

       ''' lookup13 = TRANSFER_MAP["13"]["plateWellToWellMaps"]
        lookup14 = TRANSFER_MAP["14"]["plateWellToWellMaps"]

        for src_384_well_id ,{dest_96_plate_id, dest_96_well_id}  in (lookup13) :
            for src_96_well_id ,{} in (lookup14) :
                mylookUp[src_384_well_id]= {d}'''





   

if __name__ == '__main__':
    unittest.main()
