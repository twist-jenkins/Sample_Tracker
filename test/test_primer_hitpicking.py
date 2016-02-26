
from twistdb.db import get_handle
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from twistdb.work_order import *
from twistdb.sampletrack import *
from twistdb.backend import *

import os
import os.path

operator_id = 'khervold'


def test_primer_hitpicking_src():
    desc = 'testing: primer hitpicking'
    sf_id = 'testing::primer-hitpicking-fake-salesforce-id'
    barcode = 'SPLT_KIERANPRIMERHITPICKING'
    os.environ['WEBSITE_ENV'] = 'Warp1local'

    from app import app

    script_dir = os.path.dirname(os.path.abspath(__file__))
    db = get_handle( config_file = os.path.join(script_dir, 'config.ini'))

    try:
        vector = db.query(Vector).filter(Vector.name == 'kieran-test-custom-vector').one()
    except NoResultFound:
        vector = Vector( name='kieran-test-custom-vector', vector_type='custom', sequence='ATGC',
                         id='VEC_kieran', operator_id=operator_id)

    try:
        fwd = db.query(Primer).filter(Primer.name == 'kieran-fwd-primer').one()
    except NoResultFound:
        fwd = Primer( name='kieran-fwd-primer', primer_type='custom', sequence='ATGC', direction='fwd',
                      operator_id=operator_id )
        db.add(fwd)
        db.commit()

    try:
        rev = db.query(Primer).filter(Primer.name == 'kieran-rev-primer').one()
    except NoResultFound:
        rev = Primer( name='kieran-rev-primer', primer_type='custom', sequence='ATGC', direction='rev',
                      operator_id=operator_id )
        db.add(rev)
        db.commit()

    try:
        pp = db.query(PrimerPair).filter( PrimerPair.fwd_primer==fwd, PrimerPair.rev_primer==rev ).one()
    except NoResultFound:
        pp = PrimerPair( fwd_primer=fwd, rev_primer=rev, name='kieran-primer-pair', is_active=True, primer_pair_type='custom',
                         operator_id=operator_id )
        db.add(pp)
        db.commit()

    try:
        cp = db.query(CloningProcess).filter(CloningProcess.process_name == 'kieran-test-custom').one()
    except NoResultFound:
        print '@@ before:', vector
        cp = CloningProcess( vector=vector, process_name='kieran-test-custom', operator_id=operator_id)
        db.add(cp)
        db.commit()

    try:
        order = db.query(WorkOrder).filter(WorkOrder.sf_customer_id == sf_id).one()
    except NoResultFound:
        order = WorkOrder( id='WOR_kieran', sf_customer_id=sf_id, description=desc )
        db.add(order)
        db.commit()

    print '@@ work-order:', order.id


    seq = 'GGAGAGCCTGAATTTTCTACGTGGTCACATCTTGGCCCATCAAAACTGCCGATCCGCTTTGTAGCGCGTTCTGCGGATATGGCAACCATCTCCGTTCGCGCAGGTCATAAGGAAATGGCGCTTACTGTTAGTGACATTCGGCCGTTAGCCGAACGTATCATTGAGCTGACACTGCGTCCGGCAACCGGTGCTGAACTGCCAGAGTGGACTCCGGGCGCGCACATTGATCTGGTTCTGCCTGGTGACATTATTCGCAGCTACTCTTTAACAGGGAATCTGGCCGATCGTTCGAGCTGGCGGATTGCTGTGCTGCACGAAGTGGGTGGCCGCGGGGGTAGCGATATTATTCACCGTATGAAACTGGGAGACGCTGTACGGGTTCGCTGGCCGTTAAATAACTTCGAGTTAAAACCGGCCGAATGTTACCACTTCTTCGCGTCGGGTATTGGTATCACACCGATTCTGCCGATGATTGAGGCGGCACAGCGCCAGGGACGTCCGTGTCGTCTGGACTACGTCGGCCGCTCGGGCGATCAGCTCGCGTATCTGGAACGTATTGCTGCGCTGACGGAAGCCCATGTTCACTTCACCTCGGAAACCGGGCGCCCGAACCTGAGCGAACTTCTCACTGAGTCCGGGGATGACGCAGAAGTATACGCCTGCGGTTCGGAGGGTTTCCTGCTGGATCTGGAAGCCGCTGCCACCGCCGCGGGACGGTCCTTCCACACCGAGTGGTTTGCTCCGAAGCCGGGTGCCCGTCAAGCTGCGGAGGGCGCCTTAGAAGCCTTCACGGTCCGGCTGGAACGCTCGAATCTGGAAGTTACCGTGGTTCCGGGTCAGTCTATTATCGATGCATGTGCCGAGGCCGGTGTGGTTATTCCAAGTTCTTGCTTCGAAGGGACCTGCGGATCCTGTTTGAGCACGGTTTTAGAGGGTGTTCCAGACCACCGTGATAGTTTCCTGTTACCGAACGAACGTCGTTGCAATCGGTTGATTGCACCGTGCGTGAGCAAATCGATGACCGATTGGTTGGTTCTGGACCTGTAACTCGAGCACCACCACCACCACCACTGAGATCC'

    try:
        g = db.query(DNAMolecule).filter(DNAMolecule.order==order, DNAMolecule.sequence==seq).one()
    except NoResultFound:
        g = DNAMolecule( id='SEQ_kierantest',
                         order=order, sequence=seq, order_definition='{}', line_item_number=1,
                         customer_line_item_id=desc,
                         order_item_part = db.query(OrderItemPart).filter(OrderItemPart.name == 'NHA2').one(),
                         delivery_format = db.query(DeliveryFormat).filter(DeliveryFormat.name=='tube').one(),
                         cloning_process = cp,
                         resistance_marker = db.query(ResistanceMarker).filter(ResistanceMarker.code=='AMP').one(),
                         primer_pair = pp )
        db.add(g)
        db.commit()

    design = db.query(Design).get('DES_kieran')
    if design is None:
        design = Design( id='DES_kieran', order_item=g, design='{}')
        db.add(design)
        db.commit()

    print '@@ gene:', g.id

    try:
        bg = db.query(BatchingGroup).filter(BatchingGroup.name == 'BGP_kieran').one()
    except NoResultFound:
        bg = BatchingGroup(name='BGP_kieran', version=1, customer=sf_id, order_item_type='fake',
                           cycling_conditions=99, master_mix='fake master mix')
        db.add(bg)
        db.commit()

    cluster = db.query(ClusterDesign).get('CLD_kieran')
    if cluster is None:
        cluster = ClusterDesign(id='CLD_kieran', design=design, batching_group=bg )
        db.add(cluster)
        db.commit()

    for ch in "4321":
        ext_bc = 'PLT_kierantest' + ch
        try:
            plate = db.query(Plate).filter(Plate.external_barcode==ext_bc).one()
        except NoResultFound:
            plate = Plate( operator_id=operator_id, type_id='SPTT_0006', name=ext_bc, external_barcode=ext_bc)
            db.add(plate)
            db.commit()

    print '@@ plate:', plate.id

    try:
        sample = db.query(Sample).filter(Sample.order_item == g).one()
    except NoResultFound:
        sample = Sample(order_item=g, name=desc, description=desc, operator_id=operator_id,
                        plate=plate, well=plate.get_well_by_number(1) )
        db.add(sample)
        db.commit()


    #hitpick_create_src( [{'details': {'id': barcode}}, ], [] )


def test_vector_hitpicking():
    from app import app
    from app.constants import TRANS_TYPE_VECTOR_HITPICK as VECTOR_HITPICK

    script_dir = os.path.dirname(os.path.abspath(__file__))
    db = get_handle( config_file = os.path.join(script_dir, 'config.ini'))

    data = {'sources': [{'details':{'id':'vector-bulk'}}], 'details': {'transform_type_id': VECTOR_HITPICK}, 'misc': {'dest_barcodes': ['PLT_kierantest4','PLT_kierantest1','PLT_kierantest2','PLT_kierantest3']}, 'operations': []}
    ts = TransformSpec(type_id=VECTOR_HITPICK, data_json=data, operator_id='khervold' )
    db.add(ts)
    db.commit()


    vector = db.query(Vector).filter(Vector.name == 'kieran-test-custom-vector').one()
    plate = db.query(Plate).get('SPLT_56ccf4b250e0333427700875')

    try:
        sample = db.query(Sample).filter(Sample.order_item == vector).one()
    except NoResultFound:
        sample = Sample(order_item=vector, name='link between vector "kieran-test-custom-vector" and virtual plate',
                        operator_id=operator_id, plate=plate, well=plate.get_well_by_number(1) )
        db.add(sample)
        db.commit()

if __name__ == "__main__":
    test_primer_hitpicking_src()
    test_vector_hitpicking()
