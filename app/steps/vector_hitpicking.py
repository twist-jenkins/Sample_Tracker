from collections import defaultdict
import datetime
import math
import csv
from cStringIO import StringIO
from app.routes.transform import WebError

SEARCH_LAST_N_DAYS = 2

ALIQ_VOLUME = 1.125      # [uL]
VECTOR_WASTE_VOL = 39.0  # [uL]
VECTOR_MAX_VOL = 59.0    # [uL]
ALIQ_PER_WELL = int( math.floor( (VECTOR_MAX_VOL - VECTOR_WASTE_VOL) / ALIQ_VOLUME ))


def create_src( db, vector_barcode ):
    """
    """
    from twistdb.sampletrack import Plate, TransformSpec
    from app.miseq import echo_csv
    from app.constants import TRANS_TYPE_VECTOR_HITPICK as VECTOR_HITPICK

    N_days_ago = datetime.datetime.now() - datetime.timedelta( days=SEARCH_LAST_N_DAYS )
    specjs = []
    for spec in db.query(TransformSpec) \
                  .filter( TransformSpec.date_created >= N_days_ago ):
        srcs = spec.data_json['sources']

        if ( len(srcs) == 1
             and srcs[0]['details']['id'] == vector_barcode
             and spec.data_json['details']['transform_type_id'] == VECTOR_HITPICK ):

            specjs.append( spec.data_json )

    try:
        [src_spec] = specjs
    except:
        raise WebError("expected to find 1 TransformSpec matching barcode '%s' but found %d"
                       % (vector_barcode, len(specjs)))

    dest_plates = [ db.query(Plate).filter(Plate.external_barcode == dest_plate_barcode).one()
                    for dest_plate_barcode in src_spec['misc']['dest_barcodes'] ]

    vector_tallies = defaultdict(int)
    for plate in dest_plates:
        for sample in plate.current_well_contents(db):
            # fix me: we should get vector via cloning process, which hangs off design, no?
            vector_name = sample.cloning_process.vector.name
            vector_tallies[ vector_name ] += 1

    vector_sources = {}
    for nom in vector_tallies:
        try:
            plate = db.query(Plate).filter(Plate.name == 'Virtual Vector Source :: ' + nom).one()
        except:
            raise WebError("vector source 'Virtual Vector Source :: %s' not found" % nom)
        vector_sources[ nom ] = plate

    buff = StringIO()
    rows, csv_w = [], csv.writer(buff)
    csv_w.writerow(('Vector','Well','Volume'))
    for row_i, vector_name in enumerate(sorted( vector_tallies )):
        row = chr( ord('A') + row_i )
        div = vector_tallies[ vector_name ] // ALIQ_PER_WELL
        mod = vector_tallies[ vector_name ] % ALIQ_PER_WELL
        for vol, col in ([ (VECTOR_MAX_VOL, j) for j in range(div) ]
                         + [ (VECTOR_WASTE_VOL + math.ceil(mod * ALIQ_VOLUME), div) ]):
            dest_well_name = '%s%d' % (row, col+1)
            dest_well_num = row_i * 24 + col + 1
            
            rows.append( {
                'source_plate_barcode':         vector_sources[ vector_name ].name,
                'source_well_name':             'A1',
                'source_well_number':           1,
                'source_sample_id':             vector_name,
                'source_plate_well_count':      1,
                'destination_plate_barcode':    vector_barcode,
                'destination_well_name':        dest_well_name,
                'destination_well_number':      dest_well_num,
                'destination_plate_well_count': 384,
                'destination_sample_id':        vector_name,
                'destination_plate_type':       'SPTT_0006',
            })

            csv_w.writerow( [vector_name, dest_well_name, vol] )

    buff.seek(0)
    cmds = [{"type": "PRESENT_DATA",
             "item": {
                 "type":  "csv",
                 "title": "Source Plate Map",
                 "data":  buff.read(),
             }}]

    return rows, cmds
