"""
container for PCA Primer Source Plate helper methods
used by pca_create_src and pca_master_mix functions, below
"""

from collections import defaultdict
import datetime
import math
import csv
from cStringIO import StringIO


SEARCH_LAST_N_DAYS = 2
ALIQ_PER_WELL = 390
MASTER_MIX_TEMPLATE = {
    'A1': 'Uni9_F_ex',
    'A10': 'Uni10_F_ex',
    'A11': 'Uni10_F_ex',
    'A12': 'Uni10_F_ex',
    'A13': 'Uni10_R_ex',
    'A14': 'Uni10_R_ex',
    'A15': 'Uni10_R_ex',
    'A16': 'Uni10_R_ex',
    'A17': 'Uni11_F_ex',
    'A18': 'Uni11_F_ex',
    'A19': 'Uni11_F_ex',
    'A2': 'Uni9_F_ex',
    'A20': 'Uni11_F_ex',
    'A21': 'Uni11_R_ex',
    'A22': 'Uni11_R_ex',
    'A23': 'Uni11_R_ex',
    'A24': 'Uni11_R_ex',
    'A3': 'Uni9_F_ex',
    'A4': 'Uni9_F_ex',
    'A5': 'Uni9_R_ex',
    'A6': 'Uni9_R_ex',
    'A7': 'Uni9_R_ex',
    'A8': 'Uni9_R_ex',
    'A9': 'Uni10_F_ex',
    'B1': 'Uni12_F_ex',
    'B10': 'Uni13_F_ex',
    'B11': 'Uni13_F_ex',
    'B12': 'Uni13_F_ex',
    'B13': 'Uni13_R_ex',
    'B14': 'Uni13_R_ex',
    'B15': 'Uni13_R_ex',
    'B16': 'Uni13_R_ex',
    'B17': 'Uni14_F_ex',
    'B18': 'Uni14_F_ex',
    'B19': 'Uni14_F_ex',
    'B2': 'Uni12_F_ex',
    'B20': 'Uni14_F_ex',
    'B21': 'Uni14_R_ex',
    'B22': 'Uni14_R_ex',
    'B23': 'Uni14_R_ex',
    'B24': 'Uni14_R_ex',
    'B3': 'Uni12_F_ex',
    'B4': 'Uni12_F_ex',
    'B5': 'Uni12_R_ex',
    'B6': 'Uni12_R_ex',
    'B7': 'Uni12_R_ex',
    'B8': 'Uni12_R_ex',
    'B9': 'Uni13_F_ex',
}

XFER_VOL = 0.1 # [ul]


def populate_row( starting_row, target_ct ):
    """
    @starting_row -- int representing row, eg, ord('A')
    
    returns [ ['A1','A2', ...], ['B1','B2', ...]]
    """
    container_ct = lambda tot, per: int( math.ceil( float(tot) / per ))
    wells = container_ct( target_ct, ALIQ_PER_WELL )
    grid = [[] for _ in range(container_ct( wells, 24 ))]  # in case be need multiple rows
    for i in range( wells ):
        row = chr( starting_row + (i/24) )
        col = 1 + i % 24
        grid[ i/24 ].append("%s%d" % (row,col) )
    return grid


def rows_for_custom_primers( primer_counts ):
    starting_row = ord(max(MASTER_MIX_TEMPLATE)[0]) + 1
    l = []
    for primer_name, ct in primer_counts:
        lines = populate_row(starting_row, ct)
        l.append( (primer_name, lines) )
        starting_row += len(lines)
    return l


def plate_to_custom_primers(db, plate):
    from twistdb.sampletrack import Sample

    primers, missing = defaultdict(int), set()

    for sample in db.query(Sample) \
                    .filter( Sample.plate == plate ) \
                    .order_by( Sample.plate_well_id ):
        try:
            if sample.order_item.cloning_process.vector.vector_type == 'custom':
                primers[ sample.order_item.primer_pair ] += 1
        except AttributeError as e:
            missing.add( sample )
    return primers, missing


def primer_dict( db, plates ):
    """
    generate a primer map containing both the master template and custom primers
    eg, 'Uni7_F_ex': ['A1,'A2','B1',...]
    """
    dd = defaultdict(list)
    for well, primer in MASTER_MIX_TEMPLATE.items():
        dd[primer].append(well)
    for plate in plates:
        primers, _ = plate_to_custom_primers( db, plate )
        primer_counts = [ (primer.name, primers[pp])
                          for pp in sorted(primers)
                          for primer in (pp.fwd_primer, pp.rev_primer) ]
        for primer_name, lines in rows_for_custom_primers( primer_counts ):
            for wells in lines:
                dd[primer_name].extend( wells )
    d = dict( (primer_name, sorted(l)) for primer_name, l in dd.items() )
    print '@@ primer_dict - keys:', sorted(d)
    return d

def bulk_to_temp_transform( db, bulk_plate_barcode, pca_plates ):
    """
    returns a transform for consumption by echo_csv
    """
    from twistdb.sampletrack import Sample

    pd = primer_dict( db, pca_plates )

    rows = []
    primer_ct = defaultdict(int)
    for plate in pca_plates:
        print '@@ plate:', plate.id
        for sample in db.query(Sample) \
                      .filter( Sample.plate == plate ) \
                      .order_by( Sample.plate_well_id ):
            print '@@ sample:', sample.id
            if sample.order_item and sample.order_item.primer_pair:
                for primer in (sample.order_item.primer_pair.fwd_primer,
                               sample.order_item.primer_pair.rev_primer):
                    loc = pd[ primer.name ][ primer_ct[ primer.name ] // ALIQ_PER_WELL ]
                    primer_ct[ primer.name ] += 1
                    rows.append( {
                        'source_plate_barcode':          bulk_plate_barcode,
                        'source_well_name':              loc,
                        'source_sample_id':              primer.name,  # ??
                        'source_plate_well_count':       384,
                        'destination_plate_barcode':     plate.external_barcode,
                        'destination_well_name':         plate.plate_type.get_well_name( sample.plate_well_pk ),
                        'destination_plate_well_count':  384,
                        'destination_sample_id':         sample.id,
                    })
    return rows


def bulk_barcode_to_pca_plates( db, bulk_barcode ):
    from twistdb.sampletrack import Plate, TransformSpec

    N_days_ago = datetime.datetime.now() - datetime.timedelta( days=SEARCH_LAST_N_DAYS )
    dest_barcodes = {}
    for spec in db.query(TransformSpec) \
                  .filter(TransformSpec.date_created >= N_days_ago):
        srcs = spec.data_json['sources']
        if ( len(srcs) == 1
             and srcs[0]['details']['id'] == bulk_barcode ):

            # we must maintain ordering
            for i, op in enumerate( spec.data_json['operations'] ):
                if op['destination_plate_barcode'] not in dest_barcodes:
                    dest_barcodes[ op['destination_plate_barcode'] ] = i

    assert dest_barcodes
    dest_barcodes = sorted( dest_barcodes.keys(), key=lambda s: dest_barcodes[s] )
    return [ db.query(Plate).filter(Plate.external_barcode == bc).one()
             for bc in dest_barcodes ]

def primer_src_creation( db, bulk_barcode ):
    """
    look up SampleTransformSpec based on bulk-plate barcode, and retrieve the barcodes
    of the PCA extraction plates from this record.

    then use that information to generate instructions for creating a source bulk plate
    """

    # hacky, but we currently just look @ all transforms from the last few days
    pca_plates = bulk_barcode_to_pca_plates( db, bulk_barcode )
    buff = StringIO()
    c = csv.writer(buff)
    c.writerow( ('Primer','Destination_Row') )
    for plate in pca_plates:
        primers, _ = plate_to_custom_primers( db, plate )
        primer_counts = [ (primer.name, primers[pp])
                          for pp in sorted(primers)
                          for primer in (pp.fwd_primer, pp.rev_primer) ]
        for primer_name, lines in rows_for_custom_primers( primer_counts ):
            for wells in lines:
                for well in wells:
                    c.writerow( (primer_name, well) )
    buff.seek(0)
    return buff.read()


def pca_plates_to_master_mixes( pca_plates ):
    """
    returns a list of master-mixes for the given pca plates
    assumes that each plate has one and only one condition, which can be determined by looking @ the sample in well A1
    """
    mixes = []
    for plate in pca_plates:
        try:
            # FIXME: there's a million ways this can go wrong...
            mixes.append( plate.samples[0].order_item.designs[0].cluster_designs[0].batching_group.master_mix )
        except Exception as e:
            mixes.append( 'ERROR: '+str(e) )
    return mixes


def bulk_barcode_to_mastermixes( db, bulk_barcode ):
    # FIXME: is this the right UI?  shouldn't we be using the PCA plates as input?
    
    from twistdb.sampletrack import Plate, TransformSpec
    pca_plates = bulk_barcode_to_pca_plates( db, bulk_barcode )
    return pca_plates_to_master_mixes( pca_plates )


def munge_echo_worklist( db, bulk_barcode, temp_plate_barcodes ):
    """
    retrieves transform associated with @bulk_barcode and replaces existing
    pca plate names with @temp_plate_barcodes, then returns the whole mess
    as an echo worklist
    """
    from twistdb.sampletrack import Plate, TransformSpec
    from app.miseq import echo_csv

    N_days_ago = datetime.datetime.now() - datetime.timedelta( days=SEARCH_LAST_N_DAYS )
    specs = []
    for spec in db.query(TransformSpec) \
                  .filter(TransformSpec.date_created >= N_days_ago):
        srcs = spec.data_json['sources']
        if ( len(srcs) == 1
             and srcs[0]['details']['id'] == bulk_barcode ):
            specs.append( spec.data_json )

    # there should only be one:
    [spec] = specs

    dest_barcodes = {}
    for i, op in enumerate( spec['operations'] ):
        if op['destination_plate_barcode'] not in dest_barcodes:
            dest_barcodes[ op['destination_plate_barcode'] ] = i

    assert dest_barcodes
    dest_barcodes = sorted( dest_barcodes.keys(), key=lambda s: dest_barcodes[s] )

    renaming = dict( zip( dest_barcodes, temp_plate_barcodes ))
    for op in spec['operations']:
        op['destination_plate_barcode'] = renaming[ op['destination_plate_barcode'] ]

    return echo_csv( spec['operations'], XFER_VOL )
