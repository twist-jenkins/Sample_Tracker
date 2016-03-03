from collections import defaultdict
import datetime
import math
import csv
from cStringIO import StringIO
from app.routes.transform import WebError

from twistdb.sampletrack import Plate, TransformSpec
from app.constants import (
    TRANS_TYPE_VECTOR_HITPICK as VECTOR_HITPICK,
    TRANS_TYPE_REBATCH_FOR_TRANSFORM as REBATCH_XFORM_T, )

SEARCH_LAST_N_DAYS = 2

ALIQ_VOLUME = 1.125      # [uL]
VECTOR_WASTE_VOL = 39.0  # [uL]
VECTOR_MAX_VOL = 59.0    # [uL]
ALIQ_PER_WELL = int( math.floor( (VECTOR_MAX_VOL - VECTOR_WASTE_VOL) / ALIQ_VOLUME ))

XFER_VOL = 1125 #  [nL]
ROW_WIDTH = 24 # FIXME: hard-coded for now ...


def retrieve_transform_spec( db, vector_barcode ):

    N_days_ago = datetime.datetime.now() - datetime.timedelta( days=SEARCH_LAST_N_DAYS )
    specjs = []
    for spec in db.query(TransformSpec) \
                  .filter( TransformSpec.date_created >= N_days_ago ) \
                  .filter( TransformSpec.type_id == REBATCH_XFORM_T ):
        
        if spec.data_json['details']['requestedData']['vectorSourcePlate'] == vector_barcode:
            specjs.append( spec.data_json )

    try:
        [src_spec] = specjs
    except:
        raise WebError("expected to find 1 TransformSpec matching barcode '%s' but found %d"
                       % (vector_barcode, len(specjs)))
    return src_spec


def create_src( db, vector_barcode ):
    """
    """
    src_spec = retrieve_transform_spec( db, vector_barcode )
    dest_plates = [ db.query(Plate).filter(Plate.external_barcode == x['details']['id']).one()
                    for x in src_spec['destinations'] ]

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
    row_i = 0
    for vector_name in sorted( vector_tallies ):
        div = vector_tallies[ vector_name ] // ALIQ_PER_WELL
        mod = vector_tallies[ vector_name ] % ALIQ_PER_WELL
        for vol, idx in ([ (VECTOR_MAX_VOL, j) for j in range(div) ]
                         + [ (VECTOR_WASTE_VOL + math.ceil(mod * ALIQ_VOLUME), div) ]):
            row = chr( ord('A') + row_i + (idx // ROW_WIDTH))
            col = idx % ROW_WIDTH
            dest_well_name = '%s%d' % (row, col+1)
            dest_well_num = (row_i + (idx // ROW_WIDTH)) * 24 + col + 1
            
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

        row_i += 1 + (idx // ROW_WIDTH)

    buff.seek(0)
    cmds = [{"type": "PRESENT_DATA",
             "item": {
                 "type":  "csv",
                 "title": "Source Plate Map",
                 "data":  buff.read(),
             }}]

    return rows, cmds


def hitpicking( db, vector_barcode ):
    from app.miseq import echo_csv

    src_spec = retrieve_transform_spec( db, vector_barcode )
    dest_plates = [ db.query(Plate).filter(Plate.external_barcode == dest_plate_barcode).one()
                    for dest_plate_barcode in src_spec['misc']['dest_barcodes'] ]

    vector_plate = db.query(Plate).filter(Plate.external_barcode == vector_barcode).one()

    by_vector = defaultdict(list)
    for vector_s in vector_plate.current_well_contents(db):
        print '@@ vector_s:', vector_s.id, vector_s.name, vector_s.order_item
        if vector_s.order_item:
            by_vector[ vector_s.order_item.name ].append( [vector_s.well, 0] )
        else:
            print '@@ missing vector?? sample:%s' % vector_s.id

    print '@@ vectors:', sorted((v, len(by_vector[v])) for v in by_vector)

    # order is important, as the last well will likely have less material in it
    for well_list in by_vector.values():
        well_list.sort( key=lambda (w, _): w.well_code )


    _cts = defaultdict(int)
    for dest_plate in dest_plates:
        for d_sample in dest_plate.current_well_contents(db):
            # not very efficient, but N is quite small:
            vector_name = d_sample.cloning_process.vector.name
            _cts[vector_name] += 1
    print sorted(_cts.items())
        
    rows = []
    for dest_plate in dest_plates:
        for d_sample in dest_plate.current_well_contents(db):
            # not very efficient, but N is quite small:
            vector_name = d_sample.cloning_process.vector.name
            for t in by_vector[ vector_name ]:
                if t[1] < ALIQ_PER_WELL:
                    t[1] += 1

                    rows.append({
                        'source_plate_barcode':         vector_barcode,
                        'source_well_name':             t[0].well_label,
                        'source_well_number':           t[0].well_number,
                        'source_sample_id':             vector_name,
                        'source_plate_well_count':      384,
                        'destination_plate_barcode':    dest_plate.external_barcode,
                        'destination_well_name':        d_sample.well.well_label,
                        'destination_well_number':      d_sample.well.well_number,
                        'destination_plate_well_count': 384,
                        'destination_sample_id':        d_sample.id,
                        'destination_plate_type':       'SPTT_0006',
                    })

                    break
                else:
                    #print '@@ vector:%s well:%s full (%d)' % (vector_name, t[0], t[1])
                    pass
            else:
                raise WebError("didn't find a source well for vector "+vector_name)

    return rows, [ {"type": "PRESENT_DATA",
                    "item": {
                        "type":     "file-data",
                        "title":    "Echo worklist",
                        "data":     echo_csv( rows, XFER_VOL ),
                        "mimeType": "text/csv",
                        "fileName": vector_barcode + "_echo_worklist.csv"
                    }} ]

