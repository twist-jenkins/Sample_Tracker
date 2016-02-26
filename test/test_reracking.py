import unittest
import logging
import math
import itertools
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
from json_tricks.nonp import loads
from collections import defaultdict

from twistdb.sampletrack import Plate
from twistdb.sampletrack import Sample
from test_flask_app import rnd_bc
from twistdb.sampletrack import Plate, Sample, PlateWell, PlateType
from flask import request, Response


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


    def test_calculate_volume_foreach_sample(self):

        with scoped_session(db.engine) as db_session_2:

            amp_d={}
            kan_d={}
            chlor_d={}
            unknown={}
            by_marker = defaultdict(list)
            d = {}
            rows =[]
            lookup13 ={}
            rows =[]




            #    print (qpix_plate + 1, x_48_well), ':', x_384_well_id


            #dest_type = db.session.query(PlateType).get('SPTT_0006')
            #for src_idx, src in enumerate(request.json['sources']):
                #plate_barcode = src['details']['id']
            samples = db.session.query(Plate).filter(Plate.external_barcode  == 'PLT_PCA_NORM_TEST').one().current_well_contents(db.session)


            #print len(samples)
            for sample in samples:
                concentration = sample.conc_ng_ul
                cloning_process= sample.cloning_process
                #sequence = sample.order_item.sequence
                if cloning_process is None :
                    marker = "NOMARKER"
                else:
                    marker = cloning_process.resistance_marker.code
                by_marker[ marker ].append(sample)






            '''for marker in ('AMP','KAN','CHLOR'):
                by_marker[ marker ] = ['sample-%d' % i for i in range(384)]'''



            qpix_plates =[]


            for marker in sorted (by_marker):
                tmp = defaultdict(list)
                for i, sample in enumerate(by_marker[marker]):
                    tmp[i // 48].append(sample)
                for plate_no in sorted (tmp):
                    qpix_plates.append( (marker,tmp[plate_no]) )



            dest_tmp = defaultdict(lambda: defaultdict(int))
            for i, (marker, samples) in enumerate(qpix_plates):
                dest_tmp[i // 8][ marker ] += len( samples )

            destination_plates = []
            for i, (_, markers) in enumerate(sorted(dest_tmp.items())):
                title = []
                for marker1, d in sorted(markers.items()):
                    title.append("%d samples of %s" % (d, str(marker1)))
                thisPlate = {"type": "SPTT_0006",
                                 "first_in_group": i+1,
                                 "details": {
                                     "title": "<strong> %s </strong> resistance - Plate <strong> %s </strong> of %s" %
                                              (str(marker1), (i + 1), d)}}





                destination_plates.append(thisPlate)

            #print destination_plates

        dest_plates = destination_plates
        print len(dest_plates)
        dest_type = db.session.query(PlateType).get('SPTT_0006')  # FIXME: hard-coded to 96 well
        dest_ctr = 1

        layout = test_transform(destination_plates)

        #print layout



def test_transform(dest_plates):

        lookup13 ={}
        rows =[]


        lookup13 = TRANSFER_MAP["13"]["plateWellToWellMaps"][0]
        lookup14 = TRANSFER_MAP["14"]["plateWellToWellMaps"][0]

        lookup48to384={}
        lookup384to48={}
        samples = db.session.query(Plate).filter(Plate.external_barcode  == 'PLT_PCA_NORM_TEST').one().current_well_contents(db.session)



        for x_384_well_id in lookup13:


            x_96_plate = lookup13[x_384_well_id]['destination_plate_number']
            x_96_well = lookup13[x_384_well_id]['destination_well_id']

            x_48_plate = lookup14[str(x_96_well)]['destination_plate_number']
            x_48_well = lookup14[str(x_96_well)]['destination_well_id']
            #lookup48to384

            qpix_plate = (x_96_plate - 1) * 2 + (x_48_plate - 1)

            lookup48to384[(qpix_plate + 1, x_48_well)] = x_384_well_id
            lookup384to48[x_384_well_id] = (qpix_plate + 1, x_48_well)
            print (qpix_plate + 1, x_48_well), ':', x_384_well_id



        dest_type = db.session.query(PlateType).get('SPTT_0006')
        source_type =db.session.query(PlateType).get('SPTT_0004')

        for plate in dest_plates:
            for (qpix_plate_1,x_48_well),x_384_well_id  in lookup48to384.items():




                rows.append({'source_plate_barcode':               qpix_plate_1,
                             'source_well_name':               str(source_type.get_well_by_number(int(x_48_well)).well_label),#str(samples[x_48_well].well.well_label),
                             'source_well_number':             x_48_well,#samples[x_48_well].well.well_number,
                             'source_well_code':                source_type.get_well_by_number(int(x_48_well)).well_code,#samples[x_48_well].well.well_code,
                             'source_sample_id':               str(samples[x_48_well-1].id),
                             'destination_plate_barcode':      "DDDDDD",#dest_barcodes[dest_plate_idx],
                             'destination_well_name':          str(dest_type.get_well_by_number(int(x_384_well_id)).well_label),
                             'destination_well_number':        str(x_384_well_id),
                             'destination_plate_type':         str(dest_type.type_id),
                             'destination_plate_well_count':   dest_type.layout.feature_count
                             })
        print sorted(rows)
        return rows

                       #print (qpix_plate + 1, x_48_well), ':', x_384_well_id
            #for sample in samples:
            #print (qpix_plate + 1, x_48_well), ':', x_384_well_id , ':', sample.well.well_label ,':',sample.well.well_number



'''def plates_to_rows( sources ):
    rows = []
    # Pull the first source plate to fix the plate type
    #src_plate_type = sources[0]['details']['plateDetails']['type']
    #dest_plate_type = db.session.query(PlateType).get(src_plate_type)

    samples = db.session.query(Plate).filter(Plate.external_barcode  == 'PLT_PCA_NORM_TEST').one().current_well_contents(db.session)
    for sample in samples:
        rows.append({'source_plate_barcode':           "PLT_PCA_NORM_TEST",
                     'source_well_name':               sample.well.well_label,
                     'source_well_number':             sample.well.well_number,
                     'source_well_code':               sample.well.well_code,
                     'source_sample_id':               sample.id,
                     'destination_plate_barcode':      "PLT_PCA_NORM_TEST",
                     'destination_well_name':          sample.well.well_label,
                     'destination_well_number':        sample.well.well_number,
                     'destination_plate_type':         "SPTT_0006",
                     'destination_plate_well_count':   "384"
                         })
    return rows'''






TRANSFER_MAP = loads("""
{
            "13": {  // keyed to transfer_template_id in the database
                    "description": "384 to 4x96"
                    ,"type": "standard"
                    ,"source": {
                        "plateCount": 1
                        ,"wellCount": 384
                        ,"plateTypeId": "SPTT_0006"
                        ,"variablePlateCount": false
                    }
                    ,"destination":{
                        "plateCount": 4
                        ,"wellCount": 96
                        ,"plateTypeId": "SPTT_0005"
                        ,"variablePlateCount": false
                        ,"plateTitles": ["Quadrant&nbsp;1:&nbsp;","Quadrant&nbsp;2:&nbsp;","Quadrant&nbsp;3:&nbsp;","Quadrant&nbsp;4:&nbsp;"]
                    }
                    ,"plateWellToWellMaps": [ // index in plate_well_to_well_map array = source_plate_index
                        {   // key= sopurce plate well id
                            "1": {"destination_plate_number": 1, "destination_well_id": 1}
                            ,"2": {"destination_plate_number": 2, "destination_well_id": 1}
                            ,"3": {"destination_plate_number": 1, "destination_well_id": 2}
                            ,"4": {"destination_plate_number": 2, "destination_well_id": 2}
                            ,"5": {"destination_plate_number": 1, "destination_well_id": 3}
                            ,"6": {"destination_plate_number": 2, "destination_well_id": 3}
                            ,"7": {"destination_plate_number": 1, "destination_well_id": 4}
                            ,"8": {"destination_plate_number": 2, "destination_well_id": 4}
                            ,"9": {"destination_plate_number": 1, "destination_well_id": 5}
                            ,"10": {"destination_plate_number": 2, "destination_well_id": 5}
                            ,"11": {"destination_plate_number": 1, "destination_well_id": 6}
                            ,"12": {"destination_plate_number": 2, "destination_well_id": 6}
                            ,"13": {"destination_plate_number": 1, "destination_well_id": 7}
                            ,"14": {"destination_plate_number": 2, "destination_well_id": 7}
                            ,"15": {"destination_plate_number": 1, "destination_well_id": 8}
                            ,"16": {"destination_plate_number": 2, "destination_well_id": 8}
                            ,"17": {"destination_plate_number": 1, "destination_well_id": 9}
                            ,"18": {"destination_plate_number": 2, "destination_well_id": 9}
                            ,"19": {"destination_plate_number": 1, "destination_well_id": 10}
                            ,"20": {"destination_plate_number": 2, "destination_well_id": 10}
                            ,"21": {"destination_plate_number": 1, "destination_well_id": 11}
                            ,"22": {"destination_plate_number": 2, "destination_well_id": 11}
                            ,"23": {"destination_plate_number": 1, "destination_well_id": 12}
                            ,"24": {"destination_plate_number": 2, "destination_well_id": 12}
                            ,"25": {"destination_plate_number": 3, "destination_well_id": 1}
                            ,"26": {"destination_plate_number": 4, "destination_well_id": 1}
                            ,"27": {"destination_plate_number": 3, "destination_well_id": 2}
                            ,"28": {"destination_plate_number": 4, "destination_well_id": 2}
                            ,"29": {"destination_plate_number": 3, "destination_well_id": 3}
                            ,"30": {"destination_plate_number": 4, "destination_well_id": 3}
                            ,"31": {"destination_plate_number": 3, "destination_well_id": 4}
                            ,"32": {"destination_plate_number": 4, "destination_well_id": 4}
                            ,"33": {"destination_plate_number": 3, "destination_well_id": 5}
                            ,"34": {"destination_plate_number": 4, "destination_well_id": 5}
                            ,"35": {"destination_plate_number": 3, "destination_well_id": 6}
                            ,"36": {"destination_plate_number": 4, "destination_well_id": 6}
                            ,"37": {"destination_plate_number": 3, "destination_well_id": 7}
                            ,"38": {"destination_plate_number": 4, "destination_well_id": 7}
                            ,"39": {"destination_plate_number": 3, "destination_well_id": 8}
                            ,"40": {"destination_plate_number": 4, "destination_well_id": 8}
                            ,"41": {"destination_plate_number": 3, "destination_well_id": 9}
                            ,"42": {"destination_plate_number": 4, "destination_well_id": 9}
                            ,"43": {"destination_plate_number": 3, "destination_well_id": 10}
                            ,"44": {"destination_plate_number": 4, "destination_well_id": 10}
                            ,"45": {"destination_plate_number": 3, "destination_well_id": 11}
                            ,"46": {"destination_plate_number": 4, "destination_well_id": 11}
                            ,"47": {"destination_plate_number": 3, "destination_well_id": 12}
                            ,"48": {"destination_plate_number": 4, "destination_well_id": 12}
                            ,"49": {"destination_plate_number": 1, "destination_well_id": 13}
                            ,"50": {"destination_plate_number": 2, "destination_well_id": 13}
                            ,"51": {"destination_plate_number": 1, "destination_well_id": 14}
                            ,"52": {"destination_plate_number": 2, "destination_well_id": 14}
                            ,"53": {"destination_plate_number": 1, "destination_well_id": 15}
                            ,"54": {"destination_plate_number": 2, "destination_well_id": 15}
                            ,"55": {"destination_plate_number": 1, "destination_well_id": 16}
                            ,"56": {"destination_plate_number": 2, "destination_well_id": 16}
                            ,"57": {"destination_plate_number": 1, "destination_well_id": 17}
                            ,"58": {"destination_plate_number": 2, "destination_well_id": 17}
                            ,"59": {"destination_plate_number": 1, "destination_well_id": 18}
                            ,"60": {"destination_plate_number": 2, "destination_well_id": 18}
                            ,"61": {"destination_plate_number": 1, "destination_well_id": 19}
                            ,"62": {"destination_plate_number": 2, "destination_well_id": 19}
                            ,"63": {"destination_plate_number": 1, "destination_well_id": 20}
                            ,"64": {"destination_plate_number": 2, "destination_well_id": 20}
                            ,"65": {"destination_plate_number": 1, "destination_well_id": 21}
                            ,"66": {"destination_plate_number": 2, "destination_well_id": 21}
                            ,"67": {"destination_plate_number": 1, "destination_well_id": 22}
                            ,"68": {"destination_plate_number": 2, "destination_well_id": 22}
                            ,"69": {"destination_plate_number": 1, "destination_well_id": 23}
                            ,"70": {"destination_plate_number": 2, "destination_well_id": 23}
                            ,"71": {"destination_plate_number": 1, "destination_well_id": 24}
                            ,"72": {"destination_plate_number": 2, "destination_well_id": 24}
                            ,"73": {"destination_plate_number": 3, "destination_well_id": 13}
                            ,"74": {"destination_plate_number": 4, "destination_well_id": 13}
                            ,"75": {"destination_plate_number": 3, "destination_well_id": 14}
                            ,"76": {"destination_plate_number": 4, "destination_well_id": 14}
                            ,"77": {"destination_plate_number": 3, "destination_well_id": 15}
                            ,"78": {"destination_plate_number": 4, "destination_well_id": 15}
                            ,"79": {"destination_plate_number": 3, "destination_well_id": 16}
                            ,"80": {"destination_plate_number": 4, "destination_well_id": 16}
                            ,"81": {"destination_plate_number": 3, "destination_well_id": 17}
                            ,"82": {"destination_plate_number": 4, "destination_well_id": 17}
                            ,"83": {"destination_plate_number": 3, "destination_well_id": 18}
                            ,"84": {"destination_plate_number": 4, "destination_well_id": 18}
                            ,"85": {"destination_plate_number": 3, "destination_well_id": 19}
                            ,"86": {"destination_plate_number": 4, "destination_well_id": 19}
                            ,"87": {"destination_plate_number": 3, "destination_well_id": 20}
                            ,"88": {"destination_plate_number": 4, "destination_well_id": 20}
                            ,"89": {"destination_plate_number": 3, "destination_well_id": 21}
                            ,"90": {"destination_plate_number": 4, "destination_well_id": 21}
                            ,"91": {"destination_plate_number": 3, "destination_well_id": 22}
                            ,"92": {"destination_plate_number": 4, "destination_well_id": 22}
                            ,"93": {"destination_plate_number": 3, "destination_well_id": 23}
                            ,"94": {"destination_plate_number": 4, "destination_well_id": 23}
                            ,"95": {"destination_plate_number": 3, "destination_well_id": 24}
                            ,"96": {"destination_plate_number": 4, "destination_well_id": 24}
                            ,"97": {"destination_plate_number": 1, "destination_well_id": 25}
                            ,"98": {"destination_plate_number": 2, "destination_well_id": 25}
                            ,"99": {"destination_plate_number": 1, "destination_well_id": 26}
                            ,"100": {"destination_plate_number": 2, "destination_well_id": 26}
                            ,"101": {"destination_plate_number": 1, "destination_well_id": 27}
                            ,"102": {"destination_plate_number": 2, "destination_well_id": 27}
                            ,"103": {"destination_plate_number": 1, "destination_well_id": 28}
                            ,"104": {"destination_plate_number": 2, "destination_well_id": 28}
                            ,"105": {"destination_plate_number": 1, "destination_well_id": 29}
                            ,"106": {"destination_plate_number": 2, "destination_well_id": 29}
                            ,"107": {"destination_plate_number": 1, "destination_well_id": 30}
                            ,"108": {"destination_plate_number": 2, "destination_well_id": 30}
                            ,"109": {"destination_plate_number": 1, "destination_well_id": 31}
                            ,"110": {"destination_plate_number": 2, "destination_well_id": 31}
                            ,"111": {"destination_plate_number": 1, "destination_well_id": 32}
                            ,"112": {"destination_plate_number": 2, "destination_well_id": 32}
                            ,"113": {"destination_plate_number": 1, "destination_well_id": 33}
                            ,"114": {"destination_plate_number": 2, "destination_well_id": 33}
                            ,"115": {"destination_plate_number": 1, "destination_well_id": 34}
                            ,"116": {"destination_plate_number": 2, "destination_well_id": 34}
                            ,"117": {"destination_plate_number": 1, "destination_well_id": 35}
                            ,"118": {"destination_plate_number": 2, "destination_well_id": 35}
                            ,"119": {"destination_plate_number": 1, "destination_well_id": 36}
                            ,"120": {"destination_plate_number": 2, "destination_well_id": 36}
                            ,"121": {"destination_plate_number": 3, "destination_well_id": 25}
                            ,"122": {"destination_plate_number": 4, "destination_well_id": 25}
                            ,"123": {"destination_plate_number": 3, "destination_well_id": 26}
                            ,"124": {"destination_plate_number": 4, "destination_well_id": 26}
                            ,"125": {"destination_plate_number": 3, "destination_well_id": 27}
                            ,"126": {"destination_plate_number": 4, "destination_well_id": 27}
                            ,"127": {"destination_plate_number": 3, "destination_well_id": 28}
                            ,"128": {"destination_plate_number": 4, "destination_well_id": 28}
                            ,"129": {"destination_plate_number": 3, "destination_well_id": 29}
                            ,"130": {"destination_plate_number": 4, "destination_well_id": 29}
                            ,"131": {"destination_plate_number": 3, "destination_well_id": 30}
                            ,"132": {"destination_plate_number": 4, "destination_well_id": 30}
                            ,"133": {"destination_plate_number": 3, "destination_well_id": 31}
                            ,"134": {"destination_plate_number": 4, "destination_well_id": 31}
                            ,"135": {"destination_plate_number": 3, "destination_well_id": 32}
                            ,"136": {"destination_plate_number": 4, "destination_well_id": 32}
                            ,"137": {"destination_plate_number": 3, "destination_well_id": 33}
                            ,"138": {"destination_plate_number": 4, "destination_well_id": 33}
                            ,"139": {"destination_plate_number": 3, "destination_well_id": 34}
                            ,"140": {"destination_plate_number": 4, "destination_well_id": 34}
                            ,"141": {"destination_plate_number": 3, "destination_well_id": 35}
                            ,"142": {"destination_plate_number": 4, "destination_well_id": 35}
                            ,"143": {"destination_plate_number": 3, "destination_well_id": 36}
                            ,"144": {"destination_plate_number": 4, "destination_well_id": 36}
                            ,"145": {"destination_plate_number": 1, "destination_well_id": 37}
                            ,"146": {"destination_plate_number": 2, "destination_well_id": 37}
                            ,"147": {"destination_plate_number": 1, "destination_well_id": 38}
                            ,"148": {"destination_plate_number": 2, "destination_well_id": 38}
                            ,"149": {"destination_plate_number": 1, "destination_well_id": 39}
                            ,"150": {"destination_plate_number": 2, "destination_well_id": 39}
                            ,"151": {"destination_plate_number": 1, "destination_well_id": 40}
                            ,"152": {"destination_plate_number": 2, "destination_well_id": 40}
                            ,"153": {"destination_plate_number": 1, "destination_well_id": 41}
                            ,"154": {"destination_plate_number": 2, "destination_well_id": 41}
                            ,"155": {"destination_plate_number": 1, "destination_well_id": 42}
                            ,"156": {"destination_plate_number": 2, "destination_well_id": 42}
                            ,"157": {"destination_plate_number": 1, "destination_well_id": 43}
                            ,"158": {"destination_plate_number": 2, "destination_well_id": 43}
                            ,"159": {"destination_plate_number": 1, "destination_well_id": 44}
                            ,"160": {"destination_plate_number": 2, "destination_well_id": 44}
                            ,"161": {"destination_plate_number": 1, "destination_well_id": 45}
                            ,"162": {"destination_plate_number": 2, "destination_well_id": 45}
                            ,"163": {"destination_plate_number": 1, "destination_well_id": 46}
                            ,"164": {"destination_plate_number": 2, "destination_well_id": 46}
                            ,"165": {"destination_plate_number": 1, "destination_well_id": 47}
                            ,"166": {"destination_plate_number": 2, "destination_well_id": 47}
                            ,"167": {"destination_plate_number": 1, "destination_well_id": 48}
                            ,"168": {"destination_plate_number": 2, "destination_well_id": 48}
                            ,"169": {"destination_plate_number": 3, "destination_well_id": 37}
                            ,"170": {"destination_plate_number": 4, "destination_well_id": 37}
                            ,"171": {"destination_plate_number": 3, "destination_well_id": 38}
                            ,"172": {"destination_plate_number": 4, "destination_well_id": 38}
                            ,"173": {"destination_plate_number": 3, "destination_well_id": 39}
                            ,"174": {"destination_plate_number": 4, "destination_well_id": 39}
                            ,"175": {"destination_plate_number": 3, "destination_well_id": 40}
                            ,"176": {"destination_plate_number": 4, "destination_well_id": 40}
                            ,"177": {"destination_plate_number": 3, "destination_well_id": 41}
                            ,"178": {"destination_plate_number": 4, "destination_well_id": 41}
                            ,"179": {"destination_plate_number": 3, "destination_well_id": 42}
                            ,"180": {"destination_plate_number": 4, "destination_well_id": 42}
                            ,"181": {"destination_plate_number": 3, "destination_well_id": 43}
                            ,"182": {"destination_plate_number": 4, "destination_well_id": 43}
                            ,"183": {"destination_plate_number": 3, "destination_well_id": 44}
                            ,"184": {"destination_plate_number": 4, "destination_well_id": 44}
                            ,"185": {"destination_plate_number": 3, "destination_well_id": 45}
                            ,"186": {"destination_plate_number": 4, "destination_well_id": 45}
                            ,"187": {"destination_plate_number": 3, "destination_well_id": 46}
                            ,"188": {"destination_plate_number": 4, "destination_well_id": 46}
                            ,"189": {"destination_plate_number": 3, "destination_well_id": 47}
                            ,"190": {"destination_plate_number": 4, "destination_well_id": 47}
                            ,"191": {"destination_plate_number": 3, "destination_well_id": 48}
                            ,"192": {"destination_plate_number": 4, "destination_well_id": 48}
                            ,"193": {"destination_plate_number": 1, "destination_well_id": 49}
                            ,"194": {"destination_plate_number": 2, "destination_well_id": 49}
                            ,"195": {"destination_plate_number": 1, "destination_well_id": 50}
                            ,"196": {"destination_plate_number": 2, "destination_well_id": 50}
                            ,"197": {"destination_plate_number": 1, "destination_well_id": 51}
                            ,"198": {"destination_plate_number": 2, "destination_well_id": 51}
                            ,"199": {"destination_plate_number": 1, "destination_well_id": 52}
                            ,"200": {"destination_plate_number": 2, "destination_well_id": 52}
                            ,"201": {"destination_plate_number": 1, "destination_well_id": 53}
                            ,"202": {"destination_plate_number": 2, "destination_well_id": 53}
                            ,"203": {"destination_plate_number": 1, "destination_well_id": 54}
                            ,"204": {"destination_plate_number": 2, "destination_well_id": 54}
                            ,"205": {"destination_plate_number": 1, "destination_well_id": 55}
                            ,"206": {"destination_plate_number": 2, "destination_well_id": 55}
                            ,"207": {"destination_plate_number": 1, "destination_well_id": 56}
                            ,"208": {"destination_plate_number": 2, "destination_well_id": 56}
                            ,"209": {"destination_plate_number": 1, "destination_well_id": 57}
                            ,"210": {"destination_plate_number": 2, "destination_well_id": 57}
                            ,"211": {"destination_plate_number": 1, "destination_well_id": 58}
                            ,"212": {"destination_plate_number": 2, "destination_well_id": 58}
                            ,"213": {"destination_plate_number": 1, "destination_well_id": 59}
                            ,"214": {"destination_plate_number": 2, "destination_well_id": 59}
                            ,"215": {"destination_plate_number": 1, "destination_well_id": 60}
                            ,"216": {"destination_plate_number": 2, "destination_well_id": 60}
                            ,"217": {"destination_plate_number": 3, "destination_well_id": 49}
                            ,"218": {"destination_plate_number": 4, "destination_well_id": 49}
                            ,"219": {"destination_plate_number": 3, "destination_well_id": 50}
                            ,"220": {"destination_plate_number": 4, "destination_well_id": 50}
                            ,"221": {"destination_plate_number": 3, "destination_well_id": 51}
                            ,"222": {"destination_plate_number": 4, "destination_well_id": 51}
                            ,"223": {"destination_plate_number": 3, "destination_well_id": 52}
                            ,"224": {"destination_plate_number": 4, "destination_well_id": 52}
                            ,"225": {"destination_plate_number": 3, "destination_well_id": 53}
                            ,"226": {"destination_plate_number": 4, "destination_well_id": 53}
                            ,"227": {"destination_plate_number": 3, "destination_well_id": 54}
                            ,"228": {"destination_plate_number": 4, "destination_well_id": 54}
                            ,"229": {"destination_plate_number": 3, "destination_well_id": 55}
                            ,"230": {"destination_plate_number": 4, "destination_well_id": 55}
                            ,"231": {"destination_plate_number": 3, "destination_well_id": 56}
                            ,"232": {"destination_plate_number": 4, "destination_well_id": 56}
                            ,"233": {"destination_plate_number": 3, "destination_well_id": 57}
                            ,"234": {"destination_plate_number": 4, "destination_well_id": 57}
                            ,"235": {"destination_plate_number": 3, "destination_well_id": 58}
                            ,"236": {"destination_plate_number": 4, "destination_well_id": 58}
                            ,"237": {"destination_plate_number": 3, "destination_well_id": 59}
                            ,"238": {"destination_plate_number": 4, "destination_well_id": 59}
                            ,"239": {"destination_plate_number": 3, "destination_well_id": 60}
                            ,"240": {"destination_plate_number": 4, "destination_well_id": 60}
                            ,"241": {"destination_plate_number": 1, "destination_well_id": 61}
                            ,"242": {"destination_plate_number": 2, "destination_well_id": 61}
                            ,"243": {"destination_plate_number": 1, "destination_well_id": 62}
                            ,"244": {"destination_plate_number": 2, "destination_well_id": 62}
                            ,"245": {"destination_plate_number": 1, "destination_well_id": 63}
                            ,"246": {"destination_plate_number": 2, "destination_well_id": 63}
                            ,"247": {"destination_plate_number": 1, "destination_well_id": 64}
                            ,"248": {"destination_plate_number": 2, "destination_well_id": 64}
                            ,"249": {"destination_plate_number": 1, "destination_well_id": 65}
                            ,"250": {"destination_plate_number": 2, "destination_well_id": 65}
                            ,"251": {"destination_plate_number": 1, "destination_well_id": 66}
                            ,"252": {"destination_plate_number": 2, "destination_well_id": 66}
                            ,"253": {"destination_plate_number": 1, "destination_well_id": 67}
                            ,"254": {"destination_plate_number": 2, "destination_well_id": 67}
                            ,"255": {"destination_plate_number": 1, "destination_well_id": 68}
                            ,"256": {"destination_plate_number": 2, "destination_well_id": 68}
                            ,"257": {"destination_plate_number": 1, "destination_well_id": 69}
                            ,"258": {"destination_plate_number": 2, "destination_well_id": 69}
                            ,"259": {"destination_plate_number": 1, "destination_well_id": 70}
                            ,"260": {"destination_plate_number": 2, "destination_well_id": 70}
                            ,"261": {"destination_plate_number": 1, "destination_well_id": 71}
                            ,"262": {"destination_plate_number": 2, "destination_well_id": 71}
                            ,"263": {"destination_plate_number": 1, "destination_well_id": 72}
                            ,"264": {"destination_plate_number": 2, "destination_well_id": 72}
                            ,"265": {"destination_plate_number": 3, "destination_well_id": 61}
                            ,"266": {"destination_plate_number": 4, "destination_well_id": 61}
                            ,"267": {"destination_plate_number": 3, "destination_well_id": 62}
                            ,"268": {"destination_plate_number": 4, "destination_well_id": 62}
                            ,"269": {"destination_plate_number": 3, "destination_well_id": 63}
                            ,"270": {"destination_plate_number": 4, "destination_well_id": 63}
                            ,"271": {"destination_plate_number": 3, "destination_well_id": 64}
                            ,"272": {"destination_plate_number": 4, "destination_well_id": 64}
                            ,"273": {"destination_plate_number": 3, "destination_well_id": 65}
                            ,"274": {"destination_plate_number": 4, "destination_well_id": 65}
                            ,"275": {"destination_plate_number": 3, "destination_well_id": 66}
                            ,"276": {"destination_plate_number": 4, "destination_well_id": 66}
                            ,"277": {"destination_plate_number": 3, "destination_well_id": 67}
                            ,"278": {"destination_plate_number": 4, "destination_well_id": 67}
                            ,"279": {"destination_plate_number": 3, "destination_well_id": 68}
                            ,"280": {"destination_plate_number": 4, "destination_well_id": 68}
                            ,"281": {"destination_plate_number": 3, "destination_well_id": 69}
                            ,"282": {"destination_plate_number": 4, "destination_well_id": 69}
                            ,"283": {"destination_plate_number": 3, "destination_well_id": 70}
                            ,"284": {"destination_plate_number": 4, "destination_well_id": 70}
                            ,"285": {"destination_plate_number": 3, "destination_well_id": 71}
                            ,"286": {"destination_plate_number": 4, "destination_well_id": 71}
                            ,"287": {"destination_plate_number": 3, "destination_well_id": 72}
                            ,"288": {"destination_plate_number": 4, "destination_well_id": 72}
                            ,"289": {"destination_plate_number": 1, "destination_well_id": 73}
                            ,"290": {"destination_plate_number": 2, "destination_well_id": 73}
                            ,"291": {"destination_plate_number": 1, "destination_well_id": 74}
                            ,"292": {"destination_plate_number": 2, "destination_well_id": 74}
                            ,"293": {"destination_plate_number": 1, "destination_well_id": 75}
                            ,"294": {"destination_plate_number": 2, "destination_well_id": 75}
                            ,"295": {"destination_plate_number": 1, "destination_well_id": 76}
                            ,"296": {"destination_plate_number": 2, "destination_well_id": 76}
                            ,"297": {"destination_plate_number": 1, "destination_well_id": 77}
                            ,"298": {"destination_plate_number": 2, "destination_well_id": 77}
                            ,"299": {"destination_plate_number": 1, "destination_well_id": 78}
                            ,"300": {"destination_plate_number": 2, "destination_well_id": 78}
                            ,"301": {"destination_plate_number": 1, "destination_well_id": 79}
                            ,"302": {"destination_plate_number": 2, "destination_well_id": 79}
                            ,"303": {"destination_plate_number": 1, "destination_well_id": 80}
                            ,"304": {"destination_plate_number": 2, "destination_well_id": 80}
                            ,"305": {"destination_plate_number": 1, "destination_well_id": 81}
                            ,"306": {"destination_plate_number": 2, "destination_well_id": 81}
                            ,"307": {"destination_plate_number": 1, "destination_well_id": 82}
                            ,"308": {"destination_plate_number": 2, "destination_well_id": 82}
                            ,"309": {"destination_plate_number": 1, "destination_well_id": 83}
                            ,"310": {"destination_plate_number": 2, "destination_well_id": 83}
                            ,"311": {"destination_plate_number": 1, "destination_well_id": 84}
                            ,"312": {"destination_plate_number": 2, "destination_well_id": 84}
                            ,"313": {"destination_plate_number": 3, "destination_well_id": 73}
                            ,"314": {"destination_plate_number": 4, "destination_well_id": 73}
                            ,"315": {"destination_plate_number": 3, "destination_well_id": 74}
                            ,"316": {"destination_plate_number": 4, "destination_well_id": 74}
                            ,"317": {"destination_plate_number": 3, "destination_well_id": 75}
                            ,"318": {"destination_plate_number": 4, "destination_well_id": 75}
                            ,"319": {"destination_plate_number": 3, "destination_well_id": 76}
                            ,"320": {"destination_plate_number": 4, "destination_well_id": 76}
                            ,"321": {"destination_plate_number": 3, "destination_well_id": 77}
                            ,"322": {"destination_plate_number": 4, "destination_well_id": 77}
                            ,"323": {"destination_plate_number": 3, "destination_well_id": 78}
                            ,"324": {"destination_plate_number": 4, "destination_well_id": 78}
                            ,"325": {"destination_plate_number": 3, "destination_well_id": 79}
                            ,"326": {"destination_plate_number": 4, "destination_well_id": 79}
                            ,"327": {"destination_plate_number": 3, "destination_well_id": 80}
                            ,"328": {"destination_plate_number": 4, "destination_well_id": 80}
                            ,"329": {"destination_plate_number": 3, "destination_well_id": 81}
                            ,"330": {"destination_plate_number": 4, "destination_well_id": 81}
                            ,"331": {"destination_plate_number": 3, "destination_well_id": 82}
                            ,"332": {"destination_plate_number": 4, "destination_well_id": 82}
                            ,"333": {"destination_plate_number": 3, "destination_well_id": 83}
                            ,"334": {"destination_plate_number": 4, "destination_well_id": 83}
                            ,"335": {"destination_plate_number": 3, "destination_well_id": 84}
                            ,"336": {"destination_plate_number": 4, "destination_well_id": 84}
                            ,"337": {"destination_plate_number": 1, "destination_well_id": 85}
                            ,"338": {"destination_plate_number": 2, "destination_well_id": 85}
                            ,"339": {"destination_plate_number": 1, "destination_well_id": 86}
                            ,"340": {"destination_plate_number": 2, "destination_well_id": 86}
                            ,"341": {"destination_plate_number": 1, "destination_well_id": 87}
                            ,"342": {"destination_plate_number": 2, "destination_well_id": 87}
                            ,"343": {"destination_plate_number": 1, "destination_well_id": 88}
                            ,"344": {"destination_plate_number": 2, "destination_well_id": 88}
                            ,"345": {"destination_plate_number": 1, "destination_well_id": 89}
                            ,"346": {"destination_plate_number": 2, "destination_well_id": 89}
                            ,"347": {"destination_plate_number": 1, "destination_well_id": 90}
                            ,"348": {"destination_plate_number": 2, "destination_well_id": 90}
                            ,"349": {"destination_plate_number": 1, "destination_well_id": 91}
                            ,"350": {"destination_plate_number": 2, "destination_well_id": 91}
                            ,"351": {"destination_plate_number": 1, "destination_well_id": 92}
                            ,"352": {"destination_plate_number": 2, "destination_well_id": 92}
                            ,"353": {"destination_plate_number": 1, "destination_well_id": 93}
                            ,"354": {"destination_plate_number": 2, "destination_well_id": 93}
                            ,"355": {"destination_plate_number": 1, "destination_well_id": 94}
                            ,"356": {"destination_plate_number": 2, "destination_well_id": 94}
                            ,"357": {"destination_plate_number": 1, "destination_well_id": 95}
                            ,"358": {"destination_plate_number": 2, "destination_well_id": 95}
                            ,"359": {"destination_plate_number": 1, "destination_well_id": 96}
                            ,"360": {"destination_plate_number": 2, "destination_well_id": 96}
                            ,"361": {"destination_plate_number": 3, "destination_well_id": 85}
                            ,"362": {"destination_plate_number": 4, "destination_well_id": 85}
                            ,"363": {"destination_plate_number": 3, "destination_well_id": 86}
                            ,"364": {"destination_plate_number": 4, "destination_well_id": 86}
                            ,"365": {"destination_plate_number": 3, "destination_well_id": 87}
                            ,"366": {"destination_plate_number": 4, "destination_well_id": 87}
                            ,"367": {"destination_plate_number": 3, "destination_well_id": 88}
                            ,"368": {"destination_plate_number": 4, "destination_well_id": 88}
                            ,"369": {"destination_plate_number": 3, "destination_well_id": 89}
                            ,"370": {"destination_plate_number": 4, "destination_well_id": 89}
                            ,"371": {"destination_plate_number": 3, "destination_well_id": 90}
                            ,"372": {"destination_plate_number": 4, "destination_well_id": 90}
                            ,"373": {"destination_plate_number": 3, "destination_well_id": 91}
                            ,"374": {"destination_plate_number": 4, "destination_well_id": 91}
                            ,"375": {"destination_plate_number": 3, "destination_well_id": 92}
                            ,"376": {"destination_plate_number": 4, "destination_well_id": 92}
                            ,"377": {"destination_plate_number": 3, "destination_well_id": 93}
                            ,"378": {"destination_plate_number": 4, "destination_well_id": 93}
                            ,"379": {"destination_plate_number": 3, "destination_well_id": 94}
                            ,"380": {"destination_plate_number": 4, "destination_well_id": 94}
                            ,"381": {"destination_plate_number": 3, "destination_well_id": 95}
                            ,"382": {"destination_plate_number": 4, "destination_well_id": 95}
                            ,"383": {"destination_plate_number": 3, "destination_well_id": 96}
                            ,"384": {"destination_plate_number": 4, "destination_well_id": 96}
                        }
                    ]
                }
                ,"14": {  // keyed to transfer_template_id in the database
                    "description": "96 to 2x48"
                    ,"type": "standard"
                    ,"source": {
                        "plateCount": 1
                        ,"wellCount": 96
                        ,"plateTypeId": "SPTT_0005"
                        ,"variablePlateCount": false
                    }
                    ,"destination":{
                        "plateCount": 2
                        ,"wellCount": 48
                        ,"plateTypeId": "SPTT_0004"
                        ,"variablePlateCount": false
                        ,"plateTitles": ["Left:&nbsp;&nbsp;","Right:&nbsp;"]
                    }
                    ,"plateWellToWellMaps": [ // array of source plates
                        {   // index in plate_well_to_well_map array = source_plate_index
                            "1": {"destination_plate_number": 1 ,"destination_well_id": 1}
                            ,"2": {"destination_plate_number": 1 ,"destination_well_id": 2}
                            ,"3": {"destination_plate_number": 1 ,"destination_well_id": 3}
                            ,"4": {"destination_plate_number": 1 ,"destination_well_id": 4}
                            ,"5": {"destination_plate_number": 1 ,"destination_well_id": 5}
                            ,"6": {"destination_plate_number": 1 ,"destination_well_id": 6}
                            ,"7": {"destination_plate_number": 2 ,"destination_well_id": 1}
                            ,"8": {"destination_plate_number": 2 ,"destination_well_id": 2}
                            ,"9": {"destination_plate_number": 2 ,"destination_well_id": 3}
                            ,"10": {"destination_plate_number": 2 ,"destination_well_id": 4}
                            ,"11": {"destination_plate_number": 2 ,"destination_well_id": 5}
                            ,"12": {"destination_plate_number": 2 ,"destination_well_id": 6}
                            ,"13": {"destination_plate_number": 1 ,"destination_well_id": 7}
                            ,"14": {"destination_plate_number": 1 ,"destination_well_id": 8}
                            ,"15": {"destination_plate_number": 1 ,"destination_well_id": 9}
                            ,"16": {"destination_plate_number": 1 ,"destination_well_id": 10}
                            ,"17": {"destination_plate_number": 1 ,"destination_well_id": 11}
                            ,"18": {"destination_plate_number": 1 ,"destination_well_id": 12}
                            ,"19": {"destination_plate_number": 2 ,"destination_well_id": 7}
                            ,"20": {"destination_plate_number": 2 ,"destination_well_id": 8}
                            ,"21": {"destination_plate_number": 2 ,"destination_well_id": 9}
                            ,"22": {"destination_plate_number": 2 ,"destination_well_id": 10}
                            ,"23": {"destination_plate_number": 2 ,"destination_well_id": 11}
                            ,"24": {"destination_plate_number": 2 ,"destination_well_id": 12}
                            ,"25": {"destination_plate_number": 1 ,"destination_well_id": 13}
                            ,"26": {"destination_plate_number": 1 ,"destination_well_id": 14}
                            ,"27": {"destination_plate_number": 1 ,"destination_well_id": 15}
                            ,"28": {"destination_plate_number": 1 ,"destination_well_id": 16}
                            ,"29": {"destination_plate_number": 1 ,"destination_well_id": 17}
                            ,"30": {"destination_plate_number": 1 ,"destination_well_id": 18}
                            ,"31": {"destination_plate_number": 2 ,"destination_well_id": 13}
                            ,"32": {"destination_plate_number": 2 ,"destination_well_id": 14}
                            ,"33": {"destination_plate_number": 2 ,"destination_well_id": 15}
                            ,"34": {"destination_plate_number": 2 ,"destination_well_id": 16}
                            ,"35": {"destination_plate_number": 2 ,"destination_well_id": 17}
                            ,"36": {"destination_plate_number": 2 ,"destination_well_id": 18}
                            ,"37": {"destination_plate_number": 1 ,"destination_well_id": 19}
                            ,"38": {"destination_plate_number": 1 ,"destination_well_id": 20}
                            ,"39": {"destination_plate_number": 1 ,"destination_well_id": 21}
                            ,"40": {"destination_plate_number": 1 ,"destination_well_id": 22}
                            ,"41": {"destination_plate_number": 1 ,"destination_well_id": 23}
                            ,"42": {"destination_plate_number": 1 ,"destination_well_id": 24}
                            ,"43": {"destination_plate_number": 2 ,"destination_well_id": 19}
                            ,"44": {"destination_plate_number": 2 ,"destination_well_id": 20}
                            ,"45": {"destination_plate_number": 2 ,"destination_well_id": 21}
                            ,"46": {"destination_plate_number": 2 ,"destination_well_id": 22}
                            ,"47": {"destination_plate_number": 2 ,"destination_well_id": 23}
                            ,"48": {"destination_plate_number": 2 ,"destination_well_id": 24}
                            ,"49": {"destination_plate_number": 1 ,"destination_well_id": 25}
                            ,"50": {"destination_plate_number": 1 ,"destination_well_id": 26}
                            ,"51": {"destination_plate_number": 1 ,"destination_well_id": 27}
                            ,"52": {"destination_plate_number": 1 ,"destination_well_id": 28}
                            ,"53": {"destination_plate_number": 1 ,"destination_well_id": 29}
                            ,"54": {"destination_plate_number": 1 ,"destination_well_id": 30}
                            ,"55": {"destination_plate_number": 2 ,"destination_well_id": 25}
                            ,"56": {"destination_plate_number": 2 ,"destination_well_id": 26}
                            ,"57": {"destination_plate_number": 2 ,"destination_well_id": 27}
                            ,"58": {"destination_plate_number": 2 ,"destination_well_id": 28}
                            ,"59": {"destination_plate_number": 2 ,"destination_well_id": 29}
                            ,"60": {"destination_plate_number": 2 ,"destination_well_id": 30}
                            ,"61": {"destination_plate_number": 1 ,"destination_well_id": 31}
                            ,"62": {"destination_plate_number": 1 ,"destination_well_id": 32}
                            ,"63": {"destination_plate_number": 1 ,"destination_well_id": 33}
                            ,"64": {"destination_plate_number": 1 ,"destination_well_id": 34}
                            ,"65": {"destination_plate_number": 1 ,"destination_well_id": 35}
                            ,"66": {"destination_plate_number": 1 ,"destination_well_id": 36}
                            ,"67": {"destination_plate_number": 2 ,"destination_well_id": 31}
                            ,"68": {"destination_plate_number": 2 ,"destination_well_id": 32}
                            ,"69": {"destination_plate_number": 2 ,"destination_well_id": 33}
                            ,"70": {"destination_plate_number": 2 ,"destination_well_id": 34}
                            ,"71": {"destination_plate_number": 2 ,"destination_well_id": 35}
                            ,"72": {"destination_plate_number": 2 ,"destination_well_id": 36}
                            ,"73": {"destination_plate_number": 1 ,"destination_well_id": 37}
                            ,"74": {"destination_plate_number": 1 ,"destination_well_id": 38}
                            ,"75": {"destination_plate_number": 1 ,"destination_well_id": 39}
                            ,"76": {"destination_plate_number": 1 ,"destination_well_id": 40}
                            ,"77": {"destination_plate_number": 1 ,"destination_well_id": 41}
                            ,"78": {"destination_plate_number": 1 ,"destination_well_id": 42}
                            ,"79": {"destination_plate_number": 2 ,"destination_well_id": 37}
                            ,"80": {"destination_plate_number": 2 ,"destination_well_id": 38}
                            ,"81": {"destination_plate_number": 2 ,"destination_well_id": 39}
                            ,"82": {"destination_plate_number": 2 ,"destination_well_id": 40}
                            ,"83": {"destination_plate_number": 2 ,"destination_well_id": 41}
                            ,"84": {"destination_plate_number": 2 ,"destination_well_id": 42}
                            ,"85": {"destination_plate_number": 1 ,"destination_well_id": 43}
                            ,"86": {"destination_plate_number": 1 ,"destination_well_id": 44}
                            ,"87": {"destination_plate_number": 1 ,"destination_well_id": 45}
                            ,"88": {"destination_plate_number": 1 ,"destination_well_id": 46}
                            ,"89": {"destination_plate_number": 1 ,"destination_well_id": 47}
                            ,"90": {"destination_plate_number": 1 ,"destination_well_id": 48}
                            ,"91": {"destination_plate_number": 2 ,"destination_well_id": 43}
                            ,"92": {"destination_plate_number": 2 ,"destination_well_id": 44}
                            ,"93": {"destination_plate_number": 2 ,"destination_well_id": 45}
                            ,"94": {"destination_plate_number": 2 ,"destination_well_id": 46}
                            ,"95": {"destination_plate_number": 2 ,"destination_well_id": 47}
                            ,"96": {"destination_plate_number": 2 ,"destination_well_id": 48}
                        }
                    ]
                }
            }
""")


if __name__ == '__main__':
    unittest.main()
