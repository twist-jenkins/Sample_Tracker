import datetime
from twistdb.sampletrack import *
import csv
import math
from cStringIO import StringIO
import re
from collections import defaultdict
from app.miseq import echo_csv
from app.routes.transform import WebError
from app.constants import (
    TRANS_TYPE_ECR_PCR_PLANNING as ECR_PCR_PLANNING_T )


SEARCH_LAST_N_DAYS = 2
XFER_VOL = 100 # [nl]
ALIQ_PER_WELL = 390


def retrieve_transform_spec( db, vector_barcode ):

    N_days_ago = datetime.datetime.now() - datetime.timedelta( days=SEARCH_LAST_N_DAYS )
    specjs = []

    # NOTE: we only care about the bulk : dna bindings from the "pre-planning" step
    for spec in db.query(TransformSpec) \
                  .filter( TransformSpec.date_created >= N_days_ago ) \
                  .filter( TransformSpec.type_id == ECR_PCR_PLANNING_T ):
        print '@@ spec:', spec
        srcs = spec.data_json['sources']

        if ( len(srcs) == 1
             and srcs[0]['details']['id'] == vector_barcode ):

            specjs.append( spec.data_json )

    try:
        [src_spec] = specjs
    except:
        raise WebError("expected to find 1 TransformSpec matching barcode '%s' but found %d"
                       % (vector_barcode, len(specjs)))
    return src_spec



def preplanning( db, bulk_barcode, dna_barcodes ):

    dna_plates = [ db.query(Plate).filter(Plate.external_barcode == bc).one()
                   for bc in dna_barcodes ]

    buff = StringIO()
    cout = csv.writer(buff)
    cout.writerow( ('Plate','Master_Mix') )
    for p in dna_plates:
        samples = p.current_well_contents(db)
        try:
            # FIXME: there's a million ways this can go wrong...
            cout.writerow( (p.external_barcode,
                            samples[0].order_item.designs[0].cluster_designs[0].batching_group.master_mix) )
        except Exception as e:
             cout.writerow( (p.external_barcode, e) )

    buff.seek(0)
    rows = [ {'details': {'requestedData': {'misc': {'sources': [{'details': {'id': bulk_barcode}}],
                                                     'dest_barcodes': dna_barcodes}}}} ]

    cmds = [ {"type": "PRESENT_DATA",
              "item": {
                  "type": 'csv',
                  "title": "Master Mix Needs",
                  "data": buff.read(),
              }} ]

    return rows, cmds


def create_source( db, bulk_barcode ):
    src_spec = retrieve_transform_spec( db, bulk_barcode )

    dna_plates = [ db.query(Plate).filter(Plate.external_barcode == bc).one()
                   for bc in src_spec['misc']['dest_barcodes'] ]

    primer_tallies = defaultdict(int)
    for p in dna_plates:
        for sample in p.current_well_contents(db):
            if sample.order_item.primer_pair.primer_pair_type == 'custom':
                primer_tallies[ sample.order_item.primer_pair.fwd_primer.name ] += 1
                primer_tallies[ sample.order_item.primer_pair.rev_primer.name ] += 1


    bulk_source = db.query(Plate).filter(Plate.external_barcode == 'Bulk Primer Template 1').one()

    # because primers are tracked in an odd way, we won't use the tallies for this,
    #   but instead just "transfer" everything
    rows, row_names = [], set()
    for sample in bulk_source.current_well_contents(db):
        rows.append( {
            'source_plate_barcode':         'Bulk Primer Template 1',
            'source_well_name':             sample.well.well_label,
            'source_well_number':           sample.well.well_number,
            'source_sample_id':             sample.name,
            'source_plate_well_count':      384,
            'destination_plate_barcode':    bulk_barcode,
            'destination_well_name':        sample.well.well_label,
            'destination_well_number':      sample.well.well_number,
            'destination_plate_well_count': 384,
            'destination_sample_id':        sample.name,
            'destination_plate_type':       'SPTT_0006',
        })
        row_names.add( sample.well.well_label[0] )

    row_st = ord(max(row_names)) + 1

    buff = StringIO()
    cout = csv.writer(buff)
    cout.writerow( ('Primer','Destination_Well') )

    dest_plate_type = db.query(PlateType).get('SPTT_0006')

    for i, primer_name in enumerate(sorted(primer_tallies)):
        row = chr(row_st + i)
        primer_sample = db.query(Sample).filter('link between tube and primer '+primer_name).one()
        for j in range( int(math.ceil(float(primer_tallies[primer_name]) / ALIQ_PER_WELL) )):
            dest_well_label = '%s%d' % (row, j+1)

            cout.writerow( (primer_name, dest_well_label) )

            dest_well = dest_plate_type.layout.get_well_by_label( dest_well_label )
            rows.append( {
                'source_plate_barcode':         sample.plate.external_barcode,
                'source_well_name':             primer_sample.well.well_label,
                'source_well_number':           primer_sample.well.well_number,
                'source_sample_id':             primer_sample.name,
                'source_plate_well_count':      1,
                'destination_plate_barcode':    bulk_barcode,
                'destination_well_name':        dest_well_label,
                'destination_well_number':      dest_well.well_number,
                'destination_plate_well_count': 384,
                'destination_sample_id':        primer_sample.name,
                'destination_plate_type':       'SPTT_0006',
            })

    buff.seek(0)
    return rows, [{"type": "PRESENT_DATA",
                   "item": {
                       "type": "csv",
                       "title": "Source Plate Map",
                       "data": buff.read(),
                   }    }]



def hitpicking( db, bulk_barcode, tmp_barcodes ):

    src_spec = retrieve_transform_spec( db, bulk_barcode )

    dna_plates = [ db.query(Plate).filter(Plate.external_barcode == bc).one()
                   for bc in src_spec['misc']['dest_barcodes'] ]

    bulk_plate = db.query(Plate).filter(Plate.external_barcode == bulk_barcode).one()
    
    if len( dna_plates ) != len( tmp_barcodes ):
        raise WebError("# of dna plates (%s) didn't match # of temp plates (%s)"
                       % (src_spec['misc']['dest_barcodes'], tmp_barcodes))

    primer_re = re.compile(r'primer\s(\w+)\s')
    by_primer = defaultdict(list)
    for primer_s in bulk_plate.current_well_contents(db):
        try:
            primer_name = primer_re.search( primer_s.name ).group(1)
        except Exception as e:
            print '@@', type(e), '::', e
            raise WebError("couldn't find primer name in '%s'" % s.name)

        by_primer[ primer_name ].append( [primer_s.well, 0] )

    for well_list in by_primer.values():
        well_list.sort( key=lambda (w, _): w.well_code )

    rows = []
    # these are our DNA plates
    for dna, tmp_bc in zip( dna_plates, tmp_barcodes ):
        for sample in dna.current_well_contents(db):
            # FIXME: this is awful, but currently the easiest way to get the primer
            for primer in (sample.order_item.primer_pair.fwd_primer,
                             sample.order_item.primer_pair.rev_primer):

                if primer.name not in by_primer:
                    raise WebError("didn't fine primer '%s' in bulk plate" % primer.name)

                for t in by_primer[ primer.name ]:
                    if t[1] < ALIQ_PER_WELL:
                        t[1] += 1

                        rows.append({
                            'source_plate_barcode':         bulk_barcode,
                            'source_well_name':             t[0].well_label,
                            'source_well_number':           t[0].well_number,
                            'source_sample_id':             primer.name,
                            'source_plate_well_count':      384,
                            'destination_plate_barcode':    tmp_bc,
                            'destination_well_name':        sample.well.well_label,
                            'destination_well_number':      sample.well.well_number,
                            'destination_plate_well_count': 384,
                            'destination_sample_id':        primer.name,
                            'destination_plate_type':       'SPTT_0006',
                        })

                        break
                else:
                    raise WebError("didn't find a source well for primer "+primer.name)


    return [], [ {"type": "PRESENT_DATA",
                    "item": {
                        "type":     "file-data",
                        "title":    "Echo worklist",
                        "data":     echo_csv( rows, XFER_VOL ),
                        "mimeType": "text/csv",
                        "fileName": bulk_barcode + "_echo_worklist.csv"
                    }} ]
